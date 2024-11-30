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
  MenuItem,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Divider
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import BuildIcon from '@mui/icons-material/Build';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

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

  // Group tools by category
  const toolsByCategory = tools.reduce((acc, tool) => {
    if (!acc[tool.category]) {
      acc[tool.category] = [];
    }
    acc[tool.category].push(tool);
    return acc;
  }, {});

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Create Tool Form */}
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1,
          color: 'primary.main' 
        }}>
          <AddIcon />
          Add New Tool
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Tool Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              select
              label="Category"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            >
              {categories.map((cat) => (
                <MenuItem key={cat} value={cat}>{cat}</MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleCreateTool}
              sx={{ mt: 1 }}
            >
              Create Tool
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Tools by Category */}
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1,
          color: 'primary.main',
          mb: 3 
        }}>
          <BuildIcon />
          Manage Tools
        </Typography>

        {categories.map((category) => (
          <Accordion key={category} sx={{ mb: 2 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Typography variant="h6">{category}</Typography>
                <Chip 
                  label={toolsByCategory[category]?.length || 0}
                  color="primary"
                  size="small"
                />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                {toolsByCategory[category]?.map((tool) => (
                  <Grid item xs={12} key={tool.id}>
                    <Paper 
                      elevation={1} 
                      sx={{ 
                        p: 2,
                        '&:hover': {
                          boxShadow: 3,
                          transition: 'box-shadow 0.3s ease-in-out'
                        }
                      }}
                    >
                      {editingTool === tool.id ? (
                        <Grid container spacing={2} alignItems="center">
                          <Grid item xs={12} md={4}>
                            <TextField
                              fullWidth
                              label="Tool Name"
                              value={formData.name}
                              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            />
                          </Grid>
                          <Grid item xs={12} md={4}>
                            <TextField
                              fullWidth
                              label="Description"
                              value={formData.description}
                              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            />
                          </Grid>
                          <Grid item xs={12} md={4}>
                            <Box sx={{ display: 'flex', gap: 1 }}>
                              <Button 
                                variant="contained"
                                onClick={() => handleUpdateTool(tool.id)}
                              >
                                Save
                              </Button>
                              <Button 
                                variant="outlined"
                                onClick={() => setEditingTool(null)}
                              >
                                Cancel
                              </Button>
                            </Box>
                          </Grid>
                        </Grid>
                      ) : (
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                          <Box>
                            <Typography variant="h6">{tool.name}</Typography>
                            <Typography color="text.secondary" variant="body2">
                              {tool.description}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Button 
                              startIcon={<EditIcon />}
                              onClick={() => {
                                setEditingTool(tool.id);
                                setFormData(tool);
                              }}
                              color="primary"
                              variant="outlined"
                              size="small"
                            >
                              Edit
                            </Button>
                            <Button 
                              startIcon={<DeleteIcon />}
                              onClick={() => handleDeleteTool(tool.id)}
                              color="error"
                              variant="outlined"
                              size="small"
                            >
                              Delete
                            </Button>
                          </Box>
                        </Box>
                      )}
                    </Paper>
                  </Grid>
                ))}
                {!toolsByCategory[category]?.length && (
                  <Grid item xs={12}>
                    <Typography color="text.secondary" align="center">
                      No tools in this category
                    </Typography>
                  </Grid>
                )}
              </Grid>
            </AccordionDetails>
          </Accordion>
        ))}
      </Paper>

      <Snackbar
        open={!!error || !!success}
        autoHideDuration={6000}
        onClose={() => {
          setError(null);
          setSuccess('');
        }}
      >
        <Alert 
          severity={error ? "error" : "success"} 
          sx={{ width: '100%' }}
          onClose={() => {
            setError(null);
            setSuccess('');
          }}
        >
          {error || success}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default AdminToolsPanel;
