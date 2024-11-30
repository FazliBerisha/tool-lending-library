import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  Grid,
  Typography,
  FormLabel,
  FormHelperText,
  Alert
} from '@mui/material';

const ReturnModal = ({ open, onClose, onConfirm, toolName }) => {
  const [formData, setFormData] = useState({
    condition: '',
    damages: '',
    returnReason: '',
    feedback: ''
  });
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.condition) newErrors.condition = 'Please select the tool condition';
    if (!formData.returnReason.trim()) newErrors.returnReason = 'Please provide a reason for return';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      onConfirm(formData);
      setSuccess('Return request submitted. Waiting for admin approval.');
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        Return Form: {toolName}
      </DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }}>
          Your return request will be reviewed by an admin before being finalized.
        </Alert>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <Typography variant="body2" color="text.secondary" paragraph>
              Please provide information about the tool's condition and your experience.
            </Typography>
          </Grid>
          
          <Grid item xs={12}>
            <FormControl error={!!errors.condition} fullWidth>
              <FormLabel>Tool Condition</FormLabel>
              <RadioGroup
                name="condition"
                value={formData.condition}
                onChange={handleChange}
              >
                <FormControlLabel value="excellent" control={<Radio />} label="Excellent - Like new condition" />
                <FormControlLabel value="good" control={<Radio />} label="Good - Normal wear and tear" />
                <FormControlLabel value="fair" control={<Radio />} label="Fair - Shows signs of use" />
                <FormControlLabel value="poor" control={<Radio />} label="Poor - Needs maintenance" />
              </RadioGroup>
              {errors.condition && (
                <FormHelperText>{errors.condition}</FormHelperText>
              )}
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Any Damages or Issues?"
              name="damages"
              value={formData.damages}
              onChange={handleChange}
              multiline
              rows={2}
              placeholder="Describe any damages or issues encountered (if any)"
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Reason for Return"
              name="returnReason"
              value={formData.returnReason}
              onChange={handleChange}
              error={!!errors.returnReason}
              helperText={errors.returnReason}
              required
              multiline
              rows={2}
              placeholder="Project completed? No longer needed?"
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Usage Feedback"
              name="feedback"
              value={formData.feedback}
              onChange={handleChange}
              multiline
              rows={2}
              placeholder="How was your experience with this tool? Any suggestions?"
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained" color="primary">
          Confirm Return
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ReturnModal; 