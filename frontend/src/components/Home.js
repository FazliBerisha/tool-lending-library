import React from 'react';
import { Typography, Button, Container, Grid, Paper, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import BuildIcon from '@mui/icons-material/Build';
import SearchIcon from '@mui/icons-material/Search';
import PeopleIcon from '@mui/icons-material/People';

const HeroSection = styled(Paper)(({ theme }) => ({
  backgroundColor: '#ffffff', // White background
  color: theme.palette.text.primary, // Default text color
  padding: theme.spacing(10, 0),
  marginBottom: theme.spacing(6),
}));

const HeroContent = styled(Box)(({ theme }) => ({
  textAlign: 'center',
}));

const FeatureIcon = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.secondary.main,
  color: theme.palette.secondary.contrastText,
  borderRadius: '50%',
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  display: 'inline-flex',
}));

const FeaturePaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  transition: 'transform 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-10px)',
  },
}));

const Home = () => {
  return (
    <>
      <HeroSection elevation={0}>
        <HeroContent>
          <Container>
            <Typography variant="h2" component="h1" gutterBottom>
              Welcome to Tool Lending Library
            </Typography>
            <Typography variant="h5" paragraph>
              Borrow tools, build community, and create together.
            </Typography>
            <Button variant="contained" color="secondary" size="large">
              Get Started
            </Button>
          </Container>
        </HeroContent>
      </HeroSection>

      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <FeaturePaper elevation={3}>
              <FeatureIcon>
                <BuildIcon fontSize="large" />
              </FeatureIcon>
              <Typography variant="h5" gutterBottom>
                Wide Range of Tools
              </Typography>
              <Typography>
                Access a diverse collection of tools for your projects, from power tools to gardening equipment.
              </Typography>
            </FeaturePaper>
          </Grid>
          <Grid item xs={12} md={4}>
            <FeaturePaper elevation={3}>
              <FeatureIcon>
                <SearchIcon fontSize="large" />
              </FeatureIcon>
              <Typography variant="h5" gutterBottom>
                Easy Search
              </Typography>
              <Typography>
                Find the right tool quickly with our intuitive search and filtering options.
              </Typography>
            </FeaturePaper>
          </Grid>
          <Grid item xs={12} md={4}>
            <FeaturePaper elevation={3}>
              <FeatureIcon>
                <PeopleIcon fontSize="large" />
              </FeatureIcon>
              <Typography variant="h5" gutterBottom>
                Community-Driven
              </Typography>
              <Typography>
                Join a thriving community of makers, DIY enthusiasts, and helpful neighbors.
              </Typography>
            </FeaturePaper>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default Home;
