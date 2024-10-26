import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  Snackbar,
  Grid,
  MenuItem
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

const categories = [
  'Power Tools',
  'Hand Tools',
  'Garden Tools',
  'Measurement Tools',
  'Safety Equipment'
];

const AdminToolsPanel = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: ''
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState('');
  const [tools, setTools] = useState([]);
  const [editingTool, setEditingTool] = useState(null);

  // Fetch existing tools
  const fetchTools = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/tools/');
      if (!response.ok) throw new Error('Failed to fetch tools');
      const data = await response.json();
      setTools(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchTools();
  }, []);

  const handleCreateTool = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/tools/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Failed to create tool');
      
      setSuccess('Tool created successfully!');
      setFormData({ name: '', description: '', category: '' });
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreateSampleTools = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/tools/sample', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to create sample tools');
      
      setSuccess('Sample tools created successfully!');
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  // Update tool
  const handleUpdateTool = async (toolId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/tools/${toolId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Failed to update tool');
      
      setSuccess('Tool updated successfully!');
      setEditingTool(null);
      setFormData({ name: '', description: '', category: '' });
      fetchTools(); // Refresh the list
    } catch (err) {
      setError(err.message);
    }
  };

  // Delete tool
  const handleDeleteTool = async (toolId) => {
    if (window.confirm('Are you sure you want to delete this tool?')) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://localhost:8000/api/v1/tools/${toolId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) throw new Error('Failed to delete tool');
        
        setSuccess('Tool deleted successfully!');
        fetchTools(); // Refresh the list
      } catch (err) {
        setError(err.message);
      }
    }
  };

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
          Tool Management
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Tool Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Description"
              multiline
              rows={3}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              select
              label="Category"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            >
              {categories.map((cat) => (
                <MenuItem key={cat} value={cat}>
                  {cat}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
        </Grid>

        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateTool}
          >
            Create Tool
          </Button>
          <Button
            variant="outlined"
            startIcon={<AutoAwesomeIcon />}
            onClick={handleCreateSampleTools}
          >
            Create Sample Tools
          </Button>
        </Box>

        {/* List of existing tools */}
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Existing Tools
          </Typography>
          <Grid container spacing={2}>
            {tools.map((tool) => (
              <Grid item xs={12} key={tool.id}>
                <Paper sx={{ p: 2 }}>
                  {editingTool === tool.id ? (
                    // Edit form
                    <Grid container spacing={2}>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          label="Tool Name"
                          value={formData.name}
                          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          label="Description"
                          multiline
                          rows={3}
                          value={formData.description}
                          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          select
                          label="Category"
                          value={formData.category}
                          onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                        >
                          {categories.map((cat) => (
                            <MenuItem key={cat} value={cat}>
                              {cat}
                            </MenuItem>
                          ))}
                        </TextField>
                      </Grid>
                      <Grid item xs={12}>
                        <Button onClick={() => handleUpdateTool(tool.id)}>Save</Button>
                        <Button onClick={() => setEditingTool(null)}>Cancel</Button>
                      </Grid>
                    </Grid>
                  ) : (
                    // Display tool
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Box>
                        <Typography variant="h6">{tool.name}</Typography>
                        <Typography color="textSecondary">{tool.description}</Typography>
                        <Typography color="primary">{tool.category}</Typography>
                      </Box>
                      <Box>
                        <Button 
                          onClick={() => {
                            setEditingTool(tool.id);
                            setFormData(tool);
                          }}
                        >
                          Edit
                        </Button>
                        <Button 
                          color="error"
                          onClick={() => handleDeleteTool(tool.id)}
                        >
                          Delete
                        </Button>
                      </Box>
                    </Box>
                  )}
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Paper>
    </Container>
  );
};

export default AdminToolsPanel;
