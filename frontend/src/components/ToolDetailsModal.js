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
  LinearProgress,
  Grid
} from '@mui/material';
import BuildIcon from '@mui/icons-material/Build';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import WarningIcon from '@mui/icons-material/Warning';

const ToolDetailsModal = ({ open, onClose, tool }) => {
  if (!tool) return null;

  // Calculate wear percentage (example calculation)
  const wearPercentage = tool.wear_level || 0;
  
  const getWearColor = (wear) => {
    if (wear < 30) return 'success';
    if (wear < 70) return 'warning';
    return 'error';
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <BuildIcon color="primary" />
        {tool.name}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="body1" paragraph>
              {tool.description}
            </Typography>
          </Grid>
          
          <Grid item xs={12}>
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Tool Condition
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <LinearProgress 
                  variant="determinate" 
                  value={100 - wearPercentage} 
                  color={getWearColor(wearPercentage)}
                  sx={{ flexGrow: 1 }}
                />
                <Typography variant="body2">
                  {100 - wearPercentage}%
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" gutterBottom>
              Category
            </Typography>
            <Chip label={tool.category} color="primary" size="small" />
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" gutterBottom>
              Purchase Date
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CalendarTodayIcon fontSize="small" color="action" />
              <Typography variant="body2">
                {tool.purchase_date || 'Not available'}
              </Typography>
            </Box>
          </Grid>

          {tool.maintenance_notes && (
            <Grid item xs={12}>
              <Box sx={{ mt: 2, bgcolor: 'warning.light', p: 2, borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <WarningIcon fontSize="small" />
                  Maintenance Notes
                </Typography>
                <Typography variant="body2">
                  {tool.maintenance_notes}
                </Typography>
              </Box>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
        {tool.is_available && (
          <Button variant="contained" color="primary" onClick={onClose}>
            Reserve Tool
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default ToolDetailsModal;
