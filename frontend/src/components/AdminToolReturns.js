import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Chip,
  CircularProgress,
  Card,
  CardContent,
  Button,
  Grid,
  Alert,
  Snackbar
} from '@mui/material';
import AssignmentReturnIcon from '@mui/icons-material/AssignmentReturn';

const AdminToolReturns = () => {
  const [returns, setReturns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  const fetchReturns = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/reservations/pending-returns', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch returns');
      const data = await response.json();
      setReturns(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveReturn = async (reservationId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/reservations/approve-return/${reservationId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) throw new Error('Failed to approve return');
      
      setSuccessMessage('Return approved successfully');
      // Refresh the returns list
      fetchReturns();
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchReturns();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header Section */}
      <Paper elevation={0} sx={{ p: 3, mb: 4, bgcolor: 'background.default' }}>
        <Typography variant="h4" gutterBottom sx={{ 
          fontWeight: 600,
          color: 'primary.main',
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}>
          <AssignmentReturnIcon sx={{ fontSize: 32 }} />
          Tool Returns Review
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Review and approve pending tool returns
        </Typography>
      </Paper>

      {/* Returns Counter */}
      <Paper sx={{ p: 2, mb: 3, bgcolor: '#f5f5f5' }}>
        <Typography variant="h6" color="text.secondary">
          Pending Returns: <Chip 
            label={returns.length} 
            color="primary" 
            size="small" 
            sx={{ ml: 1 }}
          />
        </Typography>
      </Paper>

      {/* Returns List */}
      <Grid container spacing={3}>
        {returns.map((reservation) => (
          <Grid item xs={12} md={6} key={reservation.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {reservation.tool.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Checked out by: {reservation.user?.username || 'Unknown User'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Reservation Date: {new Date(reservation.reservation_date).toLocaleDateString()}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => handleApproveReturn(reservation.id)}
                  >
                    Approve Return
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Error and Success Messages */}
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
      >
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      </Snackbar>

      <Snackbar
        open={!!successMessage}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage('')}
      >
        <Alert severity="success" onClose={() => setSuccessMessage('')}>
          {successMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default AdminToolReturns; 