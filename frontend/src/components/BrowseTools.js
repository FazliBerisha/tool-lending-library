import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  TextField,
  MenuItem,
  Box,
  Pagination,
  CircularProgress,
  Alert,
  InputAdornment,
  Button
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import BuildIcon from '@mui/icons-material/Build';
import { styled } from '@mui/material/styles';
import { debounce } from 'lodash'; // You might need to install lodash: npm install lodash
import { useNavigate } from 'react-router-dom';
import ToolDetailsModal from './ToolDetailsModal';

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[4],
  },
}));

const categories = [
  'All',
  'Power Tools',
  'Hand Tools',
  'Garden Tools',
  'Measurement Tools',
  'Safety Equipment'
];

const BrowseTools = () => {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('All');
  const [page, setPage] = useState(1);
  const itemsPerPage = 12;
  const navigate = useNavigate();
  const [selectedTool, setSelectedTool] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchTools = React.useCallback(async () => {
    try {
      setLoading(true);
      let url = `http://localhost:8000/api/v1/tools/?skip=${(page - 1) * itemsPerPage}&limit=${itemsPerPage}`;
      
      if (searchTerm) {
        url = `http://localhost:8000/api/v1/tools/search/?search_term=${searchTerm}`;
      } else if (category !== 'All') {
        url = `http://localhost:8000/api/v1/tools/category/${category}`;
      }

      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch tools');
      const data = await response.json();
      console.log('Fetched tools:', data);
      setTools(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [page, category, searchTerm, itemsPerPage]);

  useEffect(() => {
    fetchTools();
  }, [fetchTools]);

  // Create a debounced search function
  const debouncedSearch = useCallback(
    debounce((term) => {
      setSearchTerm(term);
    }, 300),
    []
  );

  const handleReserve = (toolId) => {
    navigate('/reservations', { state: { selectedToolId: toolId } });
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Search Tools"
              onChange={(e) => debouncedSearch(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              select
              label="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              {categories.map((cat) => (
                <MenuItem key={cat} value={cat}>
                  {cat}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
        </Grid>
      </Box>

      <Grid container spacing={3}>
        {tools.map((tool) => (
          <Grid item key={tool.id} xs={12} sm={6} md={4} lg={3}>
            <StyledCard 
              onClick={() => {
                setSelectedTool(tool);
                setIsModalOpen(true);
              }}
              sx={{ cursor: 'pointer' }}
            >
              <CardMedia
                component="div"
                sx={{
                  pt: '56.25%',
                  position: 'relative',
                  bgcolor: 'primary.light',
                }}
              >
                {tool.image_url ? (
                  <img
                    src={tool.image_url}
                    alt={tool.name}
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                    }}
                    onError={(e) => {
                      console.error('Image failed to load:', tool.image_url);
                      e.target.style.display = 'none';
                    }}
                  />
                ) : (
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: '100%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <BuildIcon sx={{ fontSize: 40, color: 'white' }} />
                  </Box>
                )}
              </CardMedia>
              <CardContent>
                <Typography gutterBottom variant="h6" component="h2">
                  {tool.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {tool.description}
                </Typography>
                <Typography variant="caption" color="primary" sx={{ mt: 1, display: 'block' }}>
                  {tool.category}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{ mt: 2 }}
                  disabled={!tool.is_available}
                  onClick={() => handleReserve(tool.id)}
                >
                  {tool.is_available ? 'Reserve' : 'Not Available'}
                </Button>
              </CardContent>
            </StyledCard>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Pagination
          count={Math.ceil(tools.length / itemsPerPage)}
          page={page}
          onChange={(e, value) => setPage(value)}
          color="primary"
        />
      </Box>

      <ToolDetailsModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        tool={selectedTool}
      />
    </Container>
  );
};

export default BrowseTools;
