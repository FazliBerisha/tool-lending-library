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
    image: null,
    brand: '',
    modelNumber: '',
    price: '',
    location: '',
    contactInfo: ''
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
      formDataToSend.append('brand', formData.brand);
      formDataToSend.append('modelNumber', formData.modelNumber);
      formDataToSend.append('price', formData.price);
      formDataToSend.append('location', formData.location);
      formDataToSend.append('contactInfo', formData.contactInfo);
      
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
        image: null,
        brand: '',
        modelNumber: '',
        price: '',
        location: '',
        contactInfo: ''
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
    <Box sx={{ 
      maxWidth: 800,
      mx: 'auto', 
      mt: 4, 
      p: 3,
      backgroundColor: '#f5f5f5',
      borderRadius: 2
    }}>
      <Paper elevation={3} sx={{ 
        p: 4,
        backgroundColor: 'white',
        borderRadius: 2,
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <Typography 
          variant="h4"
          gutterBottom 
          sx={{ 
            mb: 4, 
            textAlign: 'center',
            color: '#F4D03F',
            fontWeight: 'bold',
          }}
        >
          Submit Your Tool
        </Typography>

        <form onSubmit={handleSubmit}>
          <Box sx={{ 
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: 2,
          }}>
            <TextField
              label="Tool Name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              margin="normal"
              required
              sx={{ gridColumn: '1 / -1' }}
            />
            <TextField
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              margin="normal"
              multiline
              rows={4}
              required
              sx={{ gridColumn: '1 / -1' }}
            />
            <TextField
              select
              label="Category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              margin="normal"
              required
            >
              <MenuItem value="Hand Tools">Hand Tools</MenuItem>
              <MenuItem value="Power Tools">Power Tools</MenuItem>
              <MenuItem value="Garden Tools">Garden Tools</MenuItem>
            </TextField>
            <TextField
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
            <TextField
              label="Brand"
              name="brand"
              value={formData.brand}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              label="Model Number"
              name="modelNumber"
              value={formData.modelNumber}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              label="Price"
              name="price"
              value={formData.price}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              label="Location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              label="Contact Information"
              name="contactInfo"
              value={formData.contactInfo}
              onChange={handleChange}
              margin="normal"
              sx={{ gridColumn: '1 / -1' }}
            />
          </Box>

          <Box sx={{ 
            mt: 4,
            mb: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%'
          }}>
            <input
              accept="image/*"
              style={{ display: 'none' }}
              id="tool-image"
              type="file"
              onChange={handleImageChange}
            />
            <label htmlFor="tool-image" style={{ width: '100%', textAlign: 'center' }}>
              <Button
                variant="outlined"
                component="span"
                sx={{
                  width: '50%',
                  mb: 2,
                  borderRadius: 2,
                  borderColor: 'primary.main',
                  color: 'primary.main',
                  '&:hover': {
                    borderColor: 'primary.dark',
                    backgroundColor: 'rgba(0, 0, 0, 0.04)'
                  }
                }}
              >
                Upload Tool Image
              </Button>
            </label>
            {previewUrl && (
              <Box sx={{ 
                mt: 2, 
                textAlign: 'center',
                width: '100%',
                borderRadius: 2,
                overflow: 'hidden'
              }}>
                <img 
                  src={previewUrl} 
                  alt="Preview" 
                  style={{ 
                    maxWidth: '100%', 
                    maxHeight: '300px',
                    objectFit: 'cover',
                    borderRadius: 8
                  }} 
                />
              </Box>
            )}
          </Box>

          <Button
            type="submit"
            variant="contained"
            sx={{
              mt: 4,
              mb: 2,
              width: '50%',
              mx: 'auto',
              display: 'block',
              py: 1.5,
              backgroundColor: 'primary.main',
              '&:hover': {
                backgroundColor: 'primary.dark'
              },
              borderRadius: 2
            }}
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
