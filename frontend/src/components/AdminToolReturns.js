import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Chip,
  Snackbar,
  Alert,
  Container,
  Paper,
  Divider,
  CircularProgress,
  Avatar
} from '@mui/material';
import {
  Build as BuildIcon,
  Person as PersonIcon,
  CalendarToday as CalendarIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  AssignmentReturn as ReturnIcon
} from '@mui/icons-material';

const AdminToolReturns = () => {
  const [returns, setReturns] = useState([]);
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchReturns = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/reservations/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch returns');
      const data = await response.json();
      const pendingReturns = data.filter(res => 
        res.is_checked_out && res.return_pending
      );
      setReturns(pendingReturns);
    } catch (error) {
      setNotification({
        message: 'Failed to fetch returns',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReturn = async (returnId, action) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/reservations/return/${returnId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) throw new Error(`Failed to ${action} return`);
      
      setNotification({
        message: `Tool return ${action === 'approve' ? 'approved' : 'rejected'} successfully`,
        severity: 'success'
      });
      
      fetchReturns();
    } catch (error) {
      setNotification({
        message: `Failed to ${action} return`,
        severity: 'error'
      });
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
          <ReturnIcon sx={{ fontSize: 32 }} />
          Tool Returns Review
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Review and manage pending tool returns from users
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

      {returns.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary">
            No pending returns to review
          </Typography>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {returns.map((return_request) => (
            <Grid item xs={12} md={6} key={return_request.id}>
              <Card sx={{ 
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}>
                <CardContent>
                  {/* Tool Info */}
                  <Box display="flex" alignItems="center" mb={2}>
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                      <BuildIcon />
                    </Avatar>
                    <Box>
                      <Typography variant="h6" sx={{ mb: 0.5 }}>
                        {return_request.tool?.name}
                      </Typography>
                      <Chip 
                        label={return_request.condition || 'Condition not specified'}
                        color="primary"
                        size="small"
                      />
                    </Box>
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  {/* Return Details */}
                  <Box sx={{ mb: 2 }}>
                    {return_request.damages && (
                      <Typography variant="body2" color="error.main" paragraph>
                        <strong>Reported Damages:</strong> {return_request.damages}
                      </Typography>
                    )}
                    <Typography variant="body2" paragraph>
                      <strong>Return Reason:</strong> {return_request.return_reason || 'No reason provided'}
                    </Typography>
                    
                    <Box display="flex" gap={2} mb={2}>
                      <Chip 
                        icon={<PersonIcon />} 
                        label={`User: ${return_request.user?.username || 'Unknown'}`}
                        variant="outlined"
                        size="small"
                      />
                      <Chip 
                        icon={<CalendarIcon />}
                        label={new Date(return_request.reservation_date).toLocaleDateString()}
                        variant="outlined"
                        size="small"
                      />
                    </Box>
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  {/* Action Buttons */}
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                    <Button
                      variant="contained"
                      color="success"
                      startIcon={<CheckCircleIcon />}
                      onClick={() => handleReturn(return_request.tool_id, 'approve')}
                    >
                      Approve Return
                    </Button>
                    <Button
                      variant="contained"
                      color="error"
                      startIcon={<CancelIcon />}
                      onClick={() => handleReturn(return_request.tool_id, 'reject')}
                    >
                      Reject
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Snackbar
        open={!!notification}
        autoHideDuration={6000}
        onClose={() => setNotification(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          severity={notification?.severity} 
          onClose={() => setNotification(null)}
          variant="filled"
          elevation={6}
        >
          {notification?.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default AdminToolReturns; 