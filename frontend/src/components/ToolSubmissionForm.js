import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  MenuItem,
  Typography,
  Paper,
  Snackbar,
  Alert
} from '@mui/material';

const ToolSubmissionForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    condition: ''
  });
  const [notification, setNotification] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/tool-submissions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Failed to submit tool');

      setNotification({
        message: 'Tool submitted successfully! Waiting for admin approval.',
        severity: 'success'
      });
      setFormData({ name: '', description: '', category: '', condition: '' });
    } catch (error) {
      setNotification({
        message: 'Failed to submit tool',
        severity: 'error'
      });
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4, p: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Submit Your Tool
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Tool Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            margin="normal"
            multiline
            rows={4}
            required
          />
          <TextField
            fullWidth
            select
            label="Category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            margin="normal"
            required
          >
            <MenuItem value="power">Power Tools</MenuItem>
            <MenuItem value="hand">Hand Tools</MenuItem>
            <MenuItem value="garden">Garden Tools</MenuItem>
            {/* Add more categories as needed */}
          </TextField>
          <TextField
            fullWidth
            select
            label="Condition"
            name="condition"
            value={formData.condition}
            onChange={handleChange}
            margin="normal"
            required
          >
            <MenuItem value="new">New</MenuItem>
            <MenuItem value="excellent">Excellent</MenuItem>
            <MenuItem value="good">Good</MenuItem>
            <MenuItem value="fair">Fair</MenuItem>
          </TextField>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
            fullWidth
          >
            Submit Tool
          </Button>
        </form>
      </Paper>
      <Snackbar
        open={!!notification}
        autoHideDuration={6000}
        onClose={() => setNotification(null)}
      >
        <Alert severity={notification?.severity} onClose={() => setNotification(null)}>
          {notification?.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ToolSubmissionForm;
