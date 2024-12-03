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
    feedback: '',
    cleaningStatus: '',
    missingParts: '',
    maintenanceNeeded: '',
    nextUserNotes: '',
    actualUsageDuration: '',
    safetyIssues: ''
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
    if (!formData.actualUsageDuration.trim()) newErrors.actualUsageDuration = 'Please provide the actual usage duration';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      onConfirm(formData);
      setSuccess('Return request approved.');
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
            <FormControl error={!!errors.condition} fullWidth required>
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
              label="Actual Usage Duration"
              name="actualUsageDuration"
              value={formData.actualUsageDuration}
              onChange={handleChange}
              error={!!errors.actualUsageDuration}
              helperText={errors.actualUsageDuration}
              required
              placeholder="How long was the tool actually used? (e.g., 2 days, 5 hours)"
            />
          </Grid>

          {/* Optional Fields */}
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
              label="Usage Feedback"
              name="feedback"
              value={formData.feedback}
              onChange={handleChange}
              multiline
              rows={2}
              placeholder="How was your experience with this tool? Any suggestions?"
            />
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth>
              <FormLabel>Cleaning Status</FormLabel>
              <RadioGroup
                name="cleaningStatus"
                value={formData.cleaningStatus}
                onChange={handleChange}
              >
                <FormControlLabel value="cleaned" control={<Radio />} label="Cleaned and Ready" />
                <FormControlLabel value="needsCleaning" control={<Radio />} label="Needs Cleaning" />
                <FormControlLabel value="professional" control={<Radio />} label="Needs Professional Cleaning" />
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Missing Parts or Accessories"
              name="missingParts"
              value={formData.missingParts}
              onChange={handleChange}
              multiline
              rows={2}
              placeholder="List any missing parts or accessories"
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Maintenance Requirements"
              name="maintenanceNeeded"
              value={formData.maintenanceNeeded}
              onChange={handleChange}
              multiline
              rows={2}
              placeholder="Describe any maintenance needs (blade sharpening, battery replacement, etc.)"
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Notes for Next User"
              name="nextUserNotes"
              value={formData.nextUserNotes}
              onChange={handleChange}
              multiline
              rows={2}
              placeholder="Any tips or important information for the next user?"
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Safety Issues or Concerns"
              name="safetyIssues"
              value={formData.safetyIssues}
              onChange={handleChange}
              multiline
              rows={2}
              placeholder="Report any safety issues or concerns encountered"
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