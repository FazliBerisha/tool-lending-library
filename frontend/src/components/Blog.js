import React from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  Chip,
  Avatar,
  Button
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import BuildIcon from '@mui/icons-material/Build';
import HandymanIcon from '@mui/icons-material/Handyman';
import ConstructionIcon from '@mui/icons-material/Construction';
import HomeRepairServiceIcon from '@mui/icons-material/HomeRepairService';

const blogPosts = [
  {
    id: 1,
    title: "Essential Tools Every DIY Enthusiast Should Have",
    excerpt: "From basic hand tools to power equipment, discover the must-have tools for your home projects...",
    image: "https://images.unsplash.com/photo-1616401784845-180882ba9ba8",
    author: "Mike Thompson",
    date: "October 15, 2023",
    category: "DIY Basics",
    readTime: "5 min read",
    icon: <BuildIcon />
  },
  {
    id: 2,
    title: "Sustainable Tool Sharing: Building Community Through Lending",
    excerpt: "How tool libraries are revolutionizing resource sharing and creating stronger communities...",
    image: "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?auto=format&fit=crop&q=80",
    author: "Sarah Chen",
    date: "October 20, 2023",
    category: "Community",
    readTime: "4 min read",
    icon: <ConstructionIcon />
  },
  {
    id: 3,
    title: "Power Tool Safety: Best Practices for Home Projects",
    excerpt: "Essential safety tips and guidelines for using power tools in your DIY projects...",
    image: "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&q=80",
    author: "David Martinez",
    date: "October 25, 2023",
    category: "Safety",
    readTime: "6 min read",
    icon: <HandymanIcon />
  },
  // Optional fourth post
  {
    id: 4,
    title: "Home Workshop Setup: A Beginner's Guide",
    excerpt: "Learn how to create an efficient and safe workshop space in your home...",
    image: "https://images.unsplash.com/photo-1510074377623-8cf13fb86c08?auto=format&fit=crop&q=80",
    author: "Emma Wilson",
    date: "October 30, 2023",
    category: "Workshop",
    readTime: "7 min read",
    icon: <HomeRepairServiceIcon />
  }
];

const Blog = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg" sx={{ mt: 8, mb: 8 }}>
      {/* Featured Post */}
      <Card 
        sx={{ 
          mb: 6,
          position: 'relative',
          '&:hover': {
            transform: 'translateY(-4px)',
            transition: 'transform 0.3s ease-in-out',
          },
        }}
      >
        <CardMedia
          component="img"
          height="400"
          image="https://images.unsplash.com/photo-1416339698674-4f118dd3388b?auto=format&fit=crop&q=80"
          alt="Featured Post"
          sx={{ filter: 'brightness(0.7)' }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            bottom: 0,
            left: 0,
            right: 0,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            color: 'white',
            textAlign: 'center',
            padding: 4,
          }}
        >
          <Typography variant="overline" sx={{ mb: 2 }}>
            Featured Article
          </Typography>
          <Typography variant="h3" component="h1" sx={{ mb: 2 }}>
            The Future of Tool Sharing
          </Typography>
          <Typography variant="subtitle1" sx={{ mb: 3 }}>
            Exploring how digital platforms and community initiatives are transforming the way we access and share tools
          </Typography>
          <Button 
            variant="contained" 
            sx={{ 
              bgcolor: 'primary.main',
              color: 'white',
              '&:hover': {
                bgcolor: 'primary.dark',
              }
            }}
          >
            Read More
          </Button>
        </Box>
      </Card>

      {/* Blog Posts Grid */}
      <Grid container spacing={4}>
        {blogPosts.map((post) => (
          <Grid item xs={12} md={4} key={post.id}>
            <Card 
              sx={{ 
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  transition: 'transform 0.3s ease-in-out',
                  cursor: 'pointer'
                },
              }}
              onClick={() => navigate(`/blog/${post.id}`)}
            >
              <CardMedia
                component="img"
                height="200"
                image={post.image}
                alt={post.title}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ mb: 2 }}>
                  <Chip 
                    icon={post.icon}
                    label={post.category}
                    size="small"
                    sx={{ 
                      bgcolor: 'primary.main',
                      color: 'white',
                      '& .MuiChip-icon': {
                        color: 'white'
                      }
                    }}
                  />
                </Box>
                <Typography gutterBottom variant="h5" component="h2">
                  {post.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {post.excerpt}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 'auto' }}>
                  <Avatar sx={{ width: 32, height: 32, mr: 1 }}>
                    {post.author[0]}
                  </Avatar>
                  <Box>
                    <Typography variant="subtitle2">
                      {post.author}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {post.date} · {post.readTime}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Blog;