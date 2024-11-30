import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Chip,
  Divider
} from '@mui/material';

const ToolDetailsModal = ({ open, onClose, tool }) => {
  if (!tool) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        Tool Details
      </DialogTitle>
      <DialogContent sx={{ mt: 2 }}>
        <Typography variant="h5" gutterBottom>
          {tool.name}
        </Typography>
        
        <Box sx={{ mb: 3 }}>
          <Typography variant="body1" color="text.secondary" paragraph>
            {tool.description}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
          <Chip
            label={tool.category}
            variant="outlined"
          />
          <Chip
            label={tool.is_available ? 'Available' : 'Checked Out'}
            color={tool.is_available ? 'success' : 'error'}
          />
          <Chip
            label={`Condition: ${tool.condition || 'Not specified'}`}
            color={
              tool.condition === 'Excellent' ? 'success' :
              tool.condition === 'Good' ? 'info' :
              tool.condition === 'Fair' ? 'warning' : 'default'
            }
          />
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Submitted by
          </Typography>
          <Typography variant="body1">
            {tool.user?.username || tool.owner?.username || 'Unknown'}
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ToolDetailsModal;
