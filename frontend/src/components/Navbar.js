import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Menu, MenuItem } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import BuildIcon from '@mui/icons-material/Build';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import ArticleIcon from '@mui/icons-material/Article';
import InfoIcon from '@mui/icons-material/Info';

const Navbar = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check login status
    const checkLoginStatus = () => {
      const token = localStorage.getItem('token');
      setIsLoggedIn(!!token);
    };

    // Initial check
    checkLoginStatus();

    // Listen for changes in localStorage
    window.addEventListener('storage', checkLoginStatus);
    
    // Add a custom event listener for login status changes
    window.addEventListener('loginStateChange', checkLoginStatus);

    return () => {
      window.removeEventListener('storage', checkLoginStatus);
      window.removeEventListener('loginStateChange', checkLoginStatus);
    };
  }, []);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleProfile = () => {
    handleClose();
    navigate('/profile');
  };

  const handleLogout = () => {
    handleClose();
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('userId');
    localStorage.removeItem('role');
    
    // Dispatch custom event for navbar update
    window.dispatchEvent(new Event('loginStateChange'));
    
    setIsLoggedIn(false);
    navigate('/login');
  };

  return (
    <AppBar position="static" sx={{ 
      backgroundColor: 'transparent', 
      boxShadow: 'none',
      borderBottom: '1px solid rgba(76, 175, 80, 0.1)' // Subtle green border
    }}>
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ 
            flexGrow: 0.5,
            color: '#4caf50', // Green text
            fontWeight: 'bold'
          }}
        >
          Tool Lending Library
        </Typography>

        {/* Centered Navigation Buttons */}
        <Box sx={{ 
          position: 'absolute',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: 2
        }}>
          <Button 
            component={RouterLink} 
            to="/" 
            startIcon={<HomeIcon />}
            sx={{
              color: '#4caf50',
              borderRadius: '8px',
              padding: '6px 16px',
              position: 'relative',
              '&:hover': {
                backgroundColor: 'rgba(76, 175, 80, 0.08)',
              },
              '&::after': {
                content: '""',
                position: 'absolute',
                bottom: 0,
                left: 0,
                width: '100%',
                height: '2px',
                backgroundColor: '#4caf50',
                transform: 'scaleX(0)',
                transition: 'transform 0.3s ease-in-out',
                transformOrigin: 'center'
              },
              '&:hover::after': {
                transform: 'scaleX(1)'
              }
            }}
          >
            Home
          </Button>
          <Button 
            component={RouterLink} 
            to="/blog" 
            startIcon={<ArticleIcon />}
            sx={{
              color: '#4caf50',
              borderRadius: '8px',
              padding: '6px 16px',
              position: 'relative',
              '&:hover': {
                backgroundColor: 'rgba(76, 175, 80, 0.08)',
              },
              '&::after': {
                content: '""',
                position: 'absolute',
                bottom: 0,
                left: 0,
                width: '100%',
                height: '2px',
                backgroundColor: '#4caf50',
                transform: 'scaleX(0)',
                transition: 'transform 0.3s ease-in-out',
                transformOrigin: 'center'
              },
              '&:hover::after': {
                transform: 'scaleX(1)'
              }
            }}
          >
            Blog
          </Button>
          <Button 
            component={RouterLink} 
            to="/browse" 
            startIcon={<BuildIcon />}
            sx={{
              color: '#4caf50',
              borderRadius: '8px',
              padding: '6px 16px',
              position: 'relative',
              '&:hover': {
                backgroundColor: 'rgba(76, 175, 80, 0.08)',
              },
              '&::after': {
                content: '""',
                position: 'absolute',
                bottom: 0,
                left: 0,
                width: '100%',
                height: '2px',
                backgroundColor: '#4caf50',
                transform: 'scaleX(0)',
                transition: 'transform 0.3s ease-in-out',
                transformOrigin: 'center'
              },
              '&:hover::after': {
                transform: 'scaleX(1)'
              }
            }}
          >
            Browse Tools
          </Button>
          <Button 
            component={RouterLink} 
            to="/about" 
            startIcon={<InfoIcon />}
            sx={{
              color: '#4caf50',
              borderRadius: '8px',
              padding: '6px 16px',
              position: 'relative',
              '&:hover': {
                backgroundColor: 'rgba(76, 175, 80, 0.08)',
              },
              '&::after': {
                content: '""',
                position: 'absolute',
                bottom: 0,
                left: 0,
                width: '100%',
                height: '2px',
                backgroundColor: '#4caf50',
                transform: 'scaleX(0)',
                transition: 'transform 0.3s ease-in-out',
                transformOrigin: 'center'
              },
              '&:hover::after': {
                transform: 'scaleX(1)'
              }
            }}
          >
            About Us
          </Button>
        </Box>

        <Box sx={{ flexGrow: 1 }} />

        {/* Right-side elements */}
        {isLoggedIn ? (
          <>
            {localStorage.getItem('role') === 'admin' && (
              <Button 
                component={RouterLink} 
                to="/admin/tools" 
                startIcon={<BuildIcon />}
                sx={{
                  color: '#4caf50',
                  border: '2px solid #4caf50',
                  borderRadius: '8px',
                  marginRight: 2,
                  padding: '6px 16px',
                  '&:hover': {
                    backgroundColor: 'rgba(76, 175, 80, 0.08)',
                    borderColor: '#45a049'
                  }
                }}
              >
                Manage Tools
              </Button>
            )}
            <IconButton 
              onClick={handleMenu} 
              sx={{ 
                color: '#4caf50',
                '&:hover': {
                  backgroundColor: 'rgba(76, 175, 80, 0.08)'
                }
              }}
            >
              <AccountCircleIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleProfile}>Profile</MenuItem>
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
            <IconButton 
              sx={{ 
                color: '#4caf50',
                '&:hover': {
                  backgroundColor: 'rgba(76, 175, 80, 0.08)'
                }
              }}
            >
              <SettingsIcon />
            </IconButton>
          </>
        ) : (
          <Button 
            component={RouterLink} 
            to="/login"
            sx={{
              color: '#4caf50',
              border: '2px solid #4caf50',
              borderRadius: '8px',
              padding: '6px 16px',
              '&:hover': {
                backgroundColor: 'rgba(76, 175, 80, 0.08)',
                borderColor: '#45a049'
              }
            }}
          >
            Login
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
