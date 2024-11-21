import React from "react";
import { Typography, Button, Container, Grid, Paper, Box } from "@mui/material";
import { styled } from "@mui/material/styles";
import BuildIcon from "@mui/icons-material/Build";
import SearchIcon from "@mui/icons-material/Search";
import PeopleIcon from "@mui/icons-material/People";
import workshopImage from "../images/workshop.png";
import communityImage from "../images/community.jpg";
import sustainabilityImage from "../images/sustainability.jpg";
import { Link as RouterLink } from "react-router-dom";

const HeroSection = styled(Paper)(({ theme }) => ({
  backgroundColor: "#ffffff", // White background
  color: theme.palette.text.primary, // Default text color
  padding: theme.spacing(10, 0),
  marginBottom: theme.spacing(6),
}));

const HeroContent = styled(Box)(({ theme }) => ({
  textAlign: "center",
}));

const FeatureIcon = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.secondary.main,
  color: theme.palette.secondary.contrastText,
  borderRadius: "50%",
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  display: "inline-flex",
}));

const FeaturePaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  height: "100%",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  transition: "transform 0.3s ease-in-out",
  "&:hover": {
    transform: "translateY(-10px)",
  },
}));

const ContentSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(10, 0),
  backgroundColor: "transparent",
  scrollBehavior: "smooth",
}));

const ImageContainer = styled(Box)(({ theme }) => ({
  position: "relative",
  height: "400px",
  overflow: "hidden",
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[4],
  "& img": {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    transition: "transform 0.3s ease-in-out",
  },
  "&:hover img": {
    transform: "scale(1.05)",
  },
}));

const ContentBox = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  height: "100%",
  padding: theme.spacing(4),
}));

const Home = () => {
  return (
    <Box sx={{ overflow: "hidden" }}>
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
                Access a diverse collection of tools for your projects, from
                power tools to gardening equipment.
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
                Find the right tool quickly with our intuitive search and
                filtering options.
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
                Join a thriving community of makers, DIY enthusiasts, and
                helpful neighbors.
              </Typography>
            </FeaturePaper>
          </Grid>
        </Grid>
      </Container>

      <ContentSection>
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <ImageContainer>
                <img src={workshopImage} alt="Workshop" />
              </ImageContainer>
            </Grid>
            <Grid item xs={12} md={6}>
              <ContentBox>
                <Typography
                  variant="h3"
                  gutterBottom
                  color="primary"
                  sx={{ fontWeight: "bold" }}
                >
                  Empower Your Projects
                </Typography>
                <Typography variant="body1" paragraph>
                  Access professional-grade tools without the hefty investment.
                  Our lending library makes it possible for everyone to tackle
                  their DIY dreams, home improvements, and creative projects
                  with the right equipment.
                </Typography>
                <Button variant="outlined" color="primary" size="large">
                  Learn More
                </Button>
              </ContentBox>
            </Grid>
          </Grid>
        </Container>
      </ContentSection>

      <ContentSection sx={{ backgroundColor: "grey.50" }}>
        <Container maxWidth="lg">
          <Grid
            container
            spacing={6}
            alignItems="center"
            direction="row-reverse"
          >
            <Grid item xs={12} md={6}>
              <ImageContainer>
                <img src={communityImage} alt="Community" />
              </ImageContainer>
            </Grid>
            <Grid item xs={12} md={6}>
              <ContentBox>
                <Typography
                  variant="h3"
                  gutterBottom
                  color="primary"
                  sx={{ fontWeight: "bold" }}
                >
                  Build Community
                </Typography>
                <Typography variant="body1" paragraph>
                  Join a network of makers, creators, and DIY enthusiasts. Share
                  knowledge, exchange tips, and collaborate on projects. Our
                  platform isn't just about tools—it's about building
                  connections.
                </Typography>
                <Button variant="outlined" color="primary" size="large">
                  Join Now
                </Button>
              </ContentBox>
            </Grid>
          </Grid>
        </Container>
      </ContentSection>

      <ContentSection>
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <ImageContainer>
                <img src={sustainabilityImage} alt="Sustainability" />
              </ImageContainer>
            </Grid>
            <Grid item xs={12} md={6}>
              <ContentBox>
                <Typography
                  variant="h3"
                  gutterBottom
                  color="primary"
                  sx={{ fontWeight: "bold" }}
                >
                  Sustainable Sharing
                </Typography>
                <Typography variant="body1" paragraph>
                  By sharing resources, we reduce waste and environmental
                  impact. One quality tool shared among many is better than many
                  tools sitting idle. Join us in creating a more sustainable
                  future.
                </Typography>
                <Button variant="outlined" color="primary" size="large">
                  Our Impact
                </Button>
              </ContentBox>
            </Grid>
          </Grid>
        </Container>
      </ContentSection>

      {/* Call to Action Section */}
      <ContentSection sx={{ backgroundColor: "primary.main", color: "white" }}>
        <Container maxWidth="md" sx={{ textAlign: "center" }}>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: "bold" }}>
            Ready to Get Started?
          </Typography>
          <Typography variant="h6" paragraph sx={{ mb: 4 }}>
            Join our community today and start borrowing tools for your next
            project.
          </Typography>
          <Button
            variant="contained"
            color="secondary"
            size="large"
            component={RouterLink}
            to="/browse"
            sx={{
              px: 6,
              py: 2,
              fontSize: "1.2rem",
              "&:hover": {
                transform: "translateY(-2px)",
                boxShadow: 4,
              },
            }}
          >
            Browse Tools
          </Button>
        </Container>
      </ContentSection>
    </Box>
  );
};

export default Home;
