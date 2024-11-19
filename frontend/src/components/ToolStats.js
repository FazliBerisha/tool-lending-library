import React, { useState, useEffect } from "react";
import { Container, Paper, Typography, Grid, Box, CircularProgress, Alert } from "@mui/material";

const AdminReports = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:8000/api/v1/admin/reports", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) throw new Error("Failed to fetch report data");
        const data = await response.json();
        setReportData(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Library Usage Statistics
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} sm={6}>
            <Typography variant="h6">Total Tools</Typography>
            <Typography>{reportData.total_tools}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="h6">Available Tools</Typography>
            <Typography>{reportData.available_tools}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="h6">Reserved Tools</Typography>
            <Typography>{reportData.reserved_tools}</Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="h6">Most Reserved Tools</Typography>
            <Box>
              {reportData.most_reserved_tools.map((tool) => (
                <Typography key={tool.id}>- {tool.name}</Typography>
              ))}
            </Box>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="h6">Least Reserved Tools</Typography>
            <Box>
              {reportData.least_reserved_tools.map((tool) => (
                <Typography key={tool.id}>- {tool.name}</Typography>
              ))}
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default ToolStats;
