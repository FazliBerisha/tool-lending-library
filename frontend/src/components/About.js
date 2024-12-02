import React from 'react';
import {
  Container,
  Grid,
  Typography,
  Box,
  Card,
  CardContent,
  Avatar,
  Divider,
  Paper
} from '@mui/material';
import {
  Build as BuildIcon,
  Handshake as HandshakeIcon,
  EmojiObjects as IdeaIcon,
  GroupWork as GroupWorkIcon
} from '@mui/icons-material';

const teamMembers = [
  {
    name: "Fazli Berisha",
    role: "Founder & CEO",
    image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
    description: "Passionate about building communities through shared resources."
  },
  {
    name: "Anna Babayan",
    role: "Head of Operations",
    image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e",
    description: "Expert in tool maintenance and community engagement."
  },
  {
    name: "Farrukh Sayfiddinov",
    role: "Community Manager",
    image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80",
    description: "Dedicated to creating meaningful connections between members."
  }
];

const values = [
  {
    icon: <HandshakeIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: "Community First",
    description: "Building stronger neighborhoods through shared resources and knowledge."
  },
  {
    icon: <BuildIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: "Quality Tools",
    description: "Maintaining a curated collection of well-maintained, professional-grade equipment."
  },
  {
    icon: <IdeaIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: "Sustainability",
    description: "Reducing environmental impact through shared resources and responsible practices."
  },
  {
    icon: <GroupWorkIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: "Accessibility",
    description: "Making tools and knowledge accessible to everyone in our community."
  }
];

const About = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 8, mb: 8 }}>
      {/* Hero Section */}
      <Paper 
        elevation={0}
        sx={{ 
          bgcolor: 'primary.main',
          color: 'white',
          p: 8,
          borderRadius: 4,
          mb: 8,
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom fontWeight="bold">
          Empowering DIY Communities
        </Typography>
        <Typography variant="h5" sx={{ mb: 4, maxWidth: '800px', mx: 'auto' }}>
          We're building a world where tools and knowledge are shared resources,
          making DIY projects accessible to everyone.
        </Typography>
      </Paper>

      {/* Mission Statement */}
      <Box sx={{ mb: 8, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom color="primary.main" fontWeight="medium">
          Our Mission
        </Typography>
        <Typography variant="h6" sx={{ maxWidth: '800px', mx: 'auto' }} color="text.secondary">
          To create a sustainable, community-driven platform that makes quality tools 
          accessible to everyone while fostering a culture of sharing, learning, and 
          collaboration.
        </Typography>
      </Box>

      {/* Values Section */}
      <Box sx={{ mb: 8 }}>
        <Typography variant="h4" gutterBottom textAlign="center" color="primary.main" sx={{ mb: 4 }}>
          Our Values
        </Typography>
        <Grid container spacing={4}>
          {values.map((value, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  textAlign: 'center',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    transition: 'transform 0.3s ease-in-out',
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ mb: 2 }}>
                    {value.icon}
                  </Box>
                  <Typography variant="h6" gutterBottom>
                    {value.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {value.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Divider sx={{ mb: 8 }} />

      {/* Team Section */}
      <Box>
        <Typography variant="h4" gutterBottom textAlign="center" color="primary.main" sx={{ mb: 4 }}>
          Meet Our Team
        </Typography>
        <Grid container spacing={4}>
          {teamMembers.map((member, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  textAlign: 'center',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    transition: 'transform 0.3s ease-in-out',
                  }
                }}
              >
                <CardContent>
                  <Avatar
                    src={member.image}
                    sx={{ 
                      width: 120, 
                      height: 120, 
                      mx: 'auto', 
                      mb: 2,
                      border: 3,
                      borderColor: 'primary.main'
                    }}
                  />
                  <Typography variant="h6" gutterBottom>
                    {member.name}
                  </Typography>
                  <Typography variant="subtitle1" color="primary.main" gutterBottom>
                    {member.role}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {member.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default About;