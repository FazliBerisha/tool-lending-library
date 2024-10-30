import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  Button,
  TextField,
  Alert,
  Snackbar,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import { useLocation } from 'react-router-dom';

const ReservationPanel = () => {
  const [tools, setTools] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [selectedTool, setSelectedTool] = useState(null);
  const [reservationDate, setReservationDate] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const location = useLocation();
  const selectedToolId = location.state?.selectedToolId;
  const [selectedToolName, setSelectedToolName] = useState('');

  useEffect(() => {
    if (selectedToolId) {
      setSelectedTool(selectedToolId);
      const tool = tools.find(t => t.id === parseInt(selectedToolId));
      if (tool) {
        setSelectedToolName(tool.name);
      }
    }
  }, [selectedToolId, tools]);

  // Fetch available tools
  const fetchTools = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/tools', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch tools');
      const data = await response.json();
      setTools(data.filter(tool => tool.is_available));
    } catch (err) {
      setError(err.message);
    }
  };

  // Fetch user reservations
  const fetchReservations = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/reservations', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch reservations');
      const data = await response.json();
      setReservations(data);
    } catch (err) {
      setError(err.message);
    }
  };

  // Reserve a tool
  const handleReserve = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/reservations/reserve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          tool_id: selectedTool,
          reservation_date: reservationDate
        })
      });

      if (!response.ok) throw new Error('Failed to reserve tool');
      
      setSuccess('Tool reserved successfully!');
      setSelectedTool(null);
      setReservationDate('');
      fetchTools();
      fetchReservations();
    } catch (err) {
      setError(err.message);
    }
  };

  // Check out a tool
  const handleCheckout = async (toolId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/reservations/checkout/${toolId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to check out tool');
      
      setSuccess('Tool checked out successfully!');
      fetchReservations();
    } catch (err) {
      setError(err.message);
    }
  };

  // Return a tool
  const handleReturn = async (toolId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/reservations/return/${toolId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to return tool');
      
      setSuccess('Tool returned successfully!');
      fetchTools();
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchTools();
    fetchReservations();
  }, []);

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Snackbar
        open={!!success}
        autoHideDuration={6000}
        onClose={() => setSuccess('')}
        message={success}
      />

      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Tool Reservations
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Tool Selected"
              value={selectedToolName}
              InputProps={{
                readOnly: true,
              }}
              sx={{
                '& .MuiInputBase-input': {
                  color: selectedToolName ? 'inherit' : 'text.secondary',
                }
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              type="date"
              label="Reservation Date"
              value={reservationDate}
              onChange={(e) => setReservationDate(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleReserve}
              disabled={!selectedTool || !reservationDate}
            >
              Reserve Tool
            </Button>
          </Grid>
        </Grid>

        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
          Your Reservations
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Tool Name</TableCell>
                <TableCell>Reservation Date</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {reservations.map((reservation) => (
                <TableRow key={reservation.id}>
                  <TableCell>{reservation.tool?.name || 'Tool not found'}</TableCell>
                  <TableCell>{new Date(reservation.reservation_date).toLocaleDateString()}</TableCell>
                  <TableCell>{reservation.is_active ? 'Active' : 'Completed'}</TableCell>
                  <TableCell>
                    {reservation.is_active && (
                      <>
                        {!reservation.is_checked_out && (
                          <Button
                            variant="contained"
                            size="small"
                            onClick={() => handleCheckout(reservation.tool_id)}
                            sx={{ mr: 1 }}
                          >
                            Check Out
                          </Button>
                        )}
                        <Button
                          variant="contained"
                          color="secondary"
                          size="small"
                          onClick={() => handleReturn(reservation.tool_id)}
                        >
                          Return
                        </Button>
                      </>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Container>
  );
};

export default ReservationPanel;