import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Grid,
  TextField,
  Button,
  Avatar,
  Box,
  Divider,
  Alert,
  CircularProgress,
  Snackbar,
  IconButton
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import PersonIcon from '@mui/icons-material/Person';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import InfoIcon from '@mui/icons-material/Info';
import { styled } from '@mui/material';

const Input = styled('input')({
  display: 'none',
});

const UserProfile = () => {
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    role: '',
    full_name: '',
    bio: '',
    location: '',
    profile_picture: ''
  });

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const userId = localStorage.getItem('userId');
      const token = localStorage.getItem('token');
      
      // Use the regular profile endpoint for all users
      const response = await fetch(`http://localhost:8000/api/v1/users/profile/${userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to fetch profile');
      
      const data = await response.json();
      setProfile(data);
      setFormData({
        username: data.username,
        email: data.email,
        role: data.role,
        full_name: data.full_name,
        bio: data.bio,
        location: data.location,
        profile_picture: data.profile_picture
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    try {
      const userId = localStorage.getItem('userId');
      const token = localStorage.getItem('token');
      
      // Use the regular profile endpoint for all users
      const response = await fetch(`http://localhost:8000/api/v1/users/profile/${userId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          full_name: formData.full_name,
          bio: formData.bio,
          location: formData.location,
          profile_picture: formData.profile_picture
        })
      });

      if (!response.ok) throw new Error('Failed to update profile');
      
      const updatedProfile = await response.json();
      setProfile(updatedProfile);
      setIsEditing(false);
      setError(null);
      setSuccessMessage('Profile updated successfully!');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('image', file);

      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/users/profile-image', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formDataToSend
      });

      if (!response.ok) throw new Error('Failed to update profile image');

      const data = await response.json();
      console.log('Image upload response:', data);

      setFormData(prevData => {
        console.log('Setting form data with new image:', data.image_url);
        return {
          ...prevData,
          profile_picture: data.image_url
        };
      });

      setProfile(prevProfile => ({
        ...prevProfile,
        profile_picture: data.image_url
      }));

      const avatarImg = document.querySelector('Avatar');
      if (avatarImg) {
        avatarImg.src = data.image_url + '?' + new Date().getTime();
      }

      setSuccessMessage('Profile picture updated successfully!');
    } catch (err) {
      console.error('Image upload error:', err);
      setError('Failed to update profile picture');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Snackbar
        open={!!successMessage}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage('')}
        message={successMessage}
      />
      
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <Box position="relative">
            <Avatar 
              sx={{ 
                width: 120, 
                height: 120, 
                mr: 3,
                bgcolor: 'primary.main',
                cursor: isEditing ? 'pointer' : 'default'
              }}
              src={formData.profile_picture ? `${formData.profile_picture}?${new Date().getTime()}` : undefined}
            >
              {!formData.profile_picture && <PersonIcon sx={{ fontSize: 60 }} />}
            </Avatar>
            {isEditing && (
              <label htmlFor="profile-image-upload">
                <Input
                  accept="image/*"
                  id="profile-image-upload"
                  type="file"
                  onChange={handleImageUpload}
                />
                <IconButton
                  component="span"
                  sx={{
                    position: 'absolute',
                    bottom: 0,
                    right: 24,
                    bgcolor: 'background.paper',
                    '&:hover': {
                      bgcolor: 'primary.light',
                    },
                  }}
                  size="small"
                >
                  <PhotoCameraIcon />
                </IconButton>
              </label>
            )}
          </Box>
          <Box>
            <Typography variant="h4" gutterBottom>
              {formData.full_name || formData.username}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {formData.role}
            </Typography>
            {formData.location && (
              <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <LocationOnIcon sx={{ mr: 1, fontSize: 18 }} />
                {formData.location}
              </Typography>
            )}
          </Box>
        </Box>

        <Divider sx={{ mb: 3 }} />

        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Full Name"
              value={formData.full_name || ''}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              disabled={!isEditing}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Username"
              value={formData.username}
              disabled
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Email"
              value={formData.email}
              disabled
              type="email"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Bio"
              value={formData.bio || ''}
              onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
              disabled={!isEditing}
              multiline
              rows={3}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Location"
              value={formData.location || ''}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              disabled={!isEditing}
              InputProps={{
                startAdornment: <LocationOnIcon color="action" sx={{ mr: 1 }} />
              }}
            />
          </Grid>
        </Grid>

        <Box display="flex" justifyContent="flex-end" mt={3}>
          {!isEditing ? (
            <Button
              variant="contained"
              startIcon={<EditIcon />}
              onClick={() => setIsEditing(true)}
            >
              Edit Profile
            </Button>
          ) : (
            <>
              <Button
                variant="outlined"
                onClick={() => {
                  setIsEditing(false);
                  setFormData(profile); // Reset form data to current profile
                }}
                sx={{ mr: 2 }}
              >
                Cancel
              </Button>
              <Button
                variant="contained"
                startIcon={<SaveIcon />}
                onClick={handleUpdate}
              >
                Save Changes
              </Button>
            </>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default UserProfile;
