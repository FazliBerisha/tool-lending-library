import React, { useEffect, useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';

const AdminReport = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/api/v1/report/usage', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch statistics');
        }

        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Library Usage Statistics
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" color="primary">
              Total Tools
            </Typography>
            <Typography variant="h4">{stats.total_tools}</Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" color="primary">
              Active Reservations
            </Typography>
            <Typography variant="h4">{stats.active_reservations}</Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" color="primary">
              Total Users
            </Typography>
            <Typography variant="h4">{stats.total_users}</Typography>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AdminReport;
