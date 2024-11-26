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
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';

const AdminToolSubmissions = () => {
  const [submissions, setSubmissions] = useState([]);
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchSubmissions = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/tool-submissions/pending', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch submissions');
      const data = await response.json();
      setSubmissions(data);
    } catch (error) {
      setNotification({
        message: 'Failed to fetch submissions',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmission = async (submissionId, action) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/tool-submissions/${submissionId}/${action}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) throw new Error(`Failed to ${action} submission`);
      
      setNotification({
        message: action === 'approve' 
          ? 'Tool submission approved and added to the tool library'
          : `Tool submission ${action}d successfully`,
        severity: 'success'
      });
      
      fetchSubmissions();
    } catch (error) {
      setNotification({
        message: `Failed to ${action} submission`,
        severity: 'error'
      });
    }
  };

  useEffect(() => {
    fetchSubmissions();
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
          <TrendingUpIcon sx={{ fontSize: 32 }} />
          Tool Submissions Review
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Review and manage pending tool submissions from community members
        </Typography>
      </Paper>

      {/* Submissions Counter */}
      <Paper sx={{ p: 2, mb: 3, bgcolor: '#f5f5f5' }}>
        <Typography variant="h6" color="text.secondary">
          Pending Reviews: <Chip 
            label={submissions.length} 
            color="primary" 
            size="small" 
            sx={{ ml: 1 }}
          />
        </Typography>
      </Paper>

      {submissions.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary">
            No pending submissions to review
          </Typography>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {submissions.map((submission) => (
            <Grid item xs={12} md={6} key={submission.id}>
              <Card sx={{ 
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}>
                <CardContent>
                  {/* Tool Name and Category */}
                  <Box display="flex" alignItems="center" mb={2}>
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                      <BuildIcon />
                    </Avatar>
                    <Box>
                      <Typography variant="h6" sx={{ mb: 0.5 }}>
                        {submission.name}
                      </Typography>
                      <Chip 
                        label={submission.category.charAt(0).toUpperCase() + submission.category.slice(1)} 
                        size="small" 
                        color="primary" 
                        variant="outlined"
                      />
                    </Box>
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  {/* Submission Details */}
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body1" paragraph>
                      {submission.description}
                    </Typography>
                    <Box display="flex" gap={2} mb={2}>
                      <Chip 
                        icon={<PersonIcon />} 
                        label={`Submitted by: ${submission.user_name || 'Unknown'}`}
                        variant="outlined"
                        size="small"
                      />
                      <Chip 
                        icon={<CalendarIcon />}
                        label={new Date(submission.submitted_at).toLocaleDateString()}
                        variant="outlined"
                        size="small"
                      />
                    </Box>
                    <Chip 
                      label={`Condition: ${submission.condition.charAt(0).toUpperCase() + submission.condition.slice(1)}`}
                      color="info"
                      variant="outlined"
                      size="small"
                    />
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  {/* Action Buttons */}
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                    <Button
                      variant="contained"
                      color="success"
                      startIcon={<CheckCircleIcon />}
                      onClick={() => handleSubmission(submission.id, 'approve')}
                      sx={{
                        '&:hover': { transform: 'scale(1.02)' }
                      }}
                    >
                      Approve
                    </Button>
                    <Button
                      variant="contained"
                      color="error"
                      startIcon={<CancelIcon />}
                      onClick={() => handleSubmission(submission.id, 'reject')}
                      sx={{
                        '&:hover': { transform: 'scale(1.02)' }
                      }}
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

export default AdminToolSubmissions; 