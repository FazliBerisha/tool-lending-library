import React, { useState } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  Avatar,
  Typography,
  Snackbar,
  Alert
} from '@mui/material';
import PhotoCamera from '@mui/icons-material/PhotoCamera';

const ProfileImageUpload = () => {
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleImageChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('image', file);

      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/users/profile-image', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) throw new Error('Failed to update profile image');

      const data = await response.json();
      setPreviewUrl(data.image_url);
      setNotification({
        message: 'Profile image updated successfully',
        severity: 'success'
      });
    } catch (error) {
      setNotification({
        message: 'Failed to update profile image',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ textAlign: 'center', my: 3 }}>
      <input
        accept="image/*"
        style={{ display: 'none' }}
        id="profile-image-upload"
        type="file"
        onChange={handleImageChange}
      />
      <label htmlFor="profile-image-upload">
        <Box sx={{ mb: 2 }}>
          <Avatar
            src={previewUrl}
            sx={{ 
              width: 120, 
              height: 120, 
              margin: 'auto',
              cursor: 'pointer',
              '&:hover': { opacity: 0.8 }
            }}
          />
        </Box>
        <Button
          variant="contained"
          component="span"
          startIcon={loading ? <CircularProgress size={20} /> : <PhotoCamera />}
          disabled={loading}
        >
          Upload Profile Picture
        </Button>
      </label>

      <Snackbar
        open={!!notification}
        autoHideDuration={6000}
        onClose={() => setNotification(null)}
      >
        <Alert 
          severity={notification?.severity} 
          onClose={() => setNotification(null)}
        >
          {notification?.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ProfileImageUpload;
