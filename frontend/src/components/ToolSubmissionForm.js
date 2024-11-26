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
    condition: '',
    image: null
  });
  const [notification, setNotification] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData({ ...formData, image: file });
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formDataToSend = new FormData();
      
      // Append text fields
      formDataToSend.append('name', formData.name);
      formDataToSend.append('description', formData.description);
      formDataToSend.append('category', formData.category);
      formDataToSend.append('condition', formData.condition);
      
      // Append image if it exists
      if (formData.image) {
        formDataToSend.append('image', formData.image);
      }

      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/tool-submissions/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
          // Remove Content-Type header to let browser set it correctly for FormData
        },
        body: formDataToSend
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to submit tool');
      }

      setNotification({
        message: 'Tool submitted successfully!',
        severity: 'success'
      });
      
      // Reset form
      setFormData({
        name: '',
        description: '',
        category: '',
        condition: '',
        image: null
      });
      setPreviewUrl(null);
      
    } catch (error) {
      console.error('Submission error:', error);
      setNotification({
        message: error.message,
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
          <Box sx={{ mt: 2, mb: 2 }}>
            <input
              accept="image/*"
              style={{ display: 'none' }}
              id="tool-image"
              type="file"
              onChange={handleImageChange}
            />
            <label htmlFor="tool-image">
              <Button
                variant="outlined"
                component="span"
                fullWidth
              >
                Upload Tool Image
              </Button>
            </label>
            {previewUrl && (
              <Box sx={{ mt: 2, textAlign: 'center' }}>
                <img 
                  src={previewUrl} 
                  alt="Preview" 
                  style={{ maxWidth: '100%', maxHeight: '200px' }} 
                />
              </Box>
            )}
          </Box>
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
