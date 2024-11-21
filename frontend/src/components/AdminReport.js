import React, { useState, useEffect } from 'react';
import {
  Container, Paper, Typography, Grid, Box, CircularProgress,
  Card, CardContent, Alert, Divider
} from '@mui/material';
import {
  Build as BuildIcon,
  Warning as WarningIcon,
  Category as CategoryIcon,
  CalendarToday as CalendarIcon,
  Group as GroupIcon,
  Assignment as AssignmentIcon,
  TrendingUp as TrendingUpIcon,
  Star as StarIcon
} from '@mui/icons-material';

const StatCard = ({ icon, title, value, color = "primary", subtitle }) => (
  <Card sx={{ 
    height: '100%',
    transition: 'transform 0.2s, box-shadow 0.2s',
    '&:hover': {
      transform: 'translateY(-4px)',
      boxShadow: 4
    }
  }}>
    <CardContent>
      <Box display="flex" alignItems="center" mb={2}>
        {React.cloneElement(icon, { 
          sx: { mr: 1, fontSize: 28 }, 
          color: color 
        })}
        <Typography variant="h6" color="text.secondary">
          {title}
        </Typography>
      </Box>
      <Typography variant="h3" sx={{ mb: 1, color: `${color}.main` }}>
        {value}
      </Typography>
      {subtitle && (
        <Typography variant="body2" color="text.secondary">
          {subtitle}
        </Typography>
      )}
    </CardContent>
  </Card>
);

const AdminReport = () => {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/api/v1/admin/stats', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (!response.ok) throw new Error('Failed to fetch statistics');
        
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

  if (loading) return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
      <CircularProgress size={60} />
    </Box>
  );

  if (error) return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
    </Container>
  );

  if (!stats) return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Alert severity="info">No data available</Alert>
    </Container>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={0} sx={{ p: 3, mb: 4, bgcolor: 'background.default' }}>
        <Typography variant="h4" gutterBottom sx={{ 
          fontWeight: 600,
          color: 'primary.main',
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}>
          <TrendingUpIcon sx={{ fontSize: 32 }} />
          Dashboard Overview
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Real-time statistics and insights for your tool lending library
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12} md={4}>
          <StatCard
            icon={<BuildIcon />}
            title="Total Tools"
            value={stats.total_tools}
            color="primary"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <StatCard
            icon={<AssignmentIcon />}
            title="Active Reservations"
            value={stats.active_reservations}
            color="success"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <StatCard
            icon={<GroupIcon />}
            title="Total Users"
            value={stats.total_users}
            color="info"
          />
        </Grid>

        {/* Tool Availability Section */}
        {stats.tool_stats && (
          <>
            <Grid item xs={12}>
              <Divider sx={{ my: 4 }}>
                <Typography variant="h6" color="text.secondary" sx={{ px: 2 }}>
                  Tool Availability
                </Typography>
              </Divider>
            </Grid>

            <Grid item xs={12} md={6}>
              <StatCard
                icon={<BuildIcon />}
                title="Available Tools"
                value={stats.tool_stats.available}
                color="success"
                subtitle="Ready for reservation"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <StatCard
                icon={<WarningIcon />}
                title="Checked Out Tools"
                value={stats.tool_stats.checked_out}
                color="warning"
                subtitle="Currently in use"
              />
            </Grid>
          </>
        )}

        {/* Activity Metrics */}
        <Grid item xs={12}>
          <Divider sx={{ my: 4 }}>
            <Typography variant="h6" color="text.secondary" sx={{ px: 2 }}>
              Activity Metrics
            </Typography>
          </Divider>
        </Grid>

        <Grid item xs={12} md={6}>
          <StatCard
            icon={<CalendarIcon />}
            title="30-Day Reservations"
            value={stats.monthly_reservations}
            color="info"
            subtitle="Reservations in the last month"
          />
        </Grid>

        {/* Active Users Section */}
        {stats.active_users && stats.active_users.length > 0 && (
          <>
            <Grid item xs={12}>
              <Divider sx={{ my: 4 }}>
                <Typography variant="h6" color="text.secondary" sx={{ px: 2 }}>
                  Top Users
                </Typography>
              </Divider>
            </Grid>

            {stats.active_users.map((user, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card sx={{ 
                  height: '100%',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}>
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      <StarIcon sx={{ mr: 1, color: 'warning.main' }} />
                      <Typography variant="h6" color="text.secondary">
                        {user.username}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color="warning.main">
                      {user.reservations}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Reservations
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </>
        )}
      </Grid>
    </Container>
  );
};

export default AdminReport;
