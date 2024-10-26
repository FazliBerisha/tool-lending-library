import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Menu, MenuItem } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import BuildIcon from '@mui/icons-material/Build';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';

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
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Tool Lending Library
        </Typography>
        <Button color="inherit" component={RouterLink} to="/" startIcon={<HomeIcon />}>
          Home
        </Button>
        <Button color="inherit" component={RouterLink} to="/browse" startIcon={<BuildIcon />}>
          Browse Tools
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        {isLoggedIn ? (
          <>
            <IconButton color="inherit" onClick={handleMenu} aria-label="account">
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
            <IconButton color="inherit" aria-label="settings">
              <SettingsIcon />
            </IconButton>
          </>
        ) : (
          <Button color="inherit" component={RouterLink} to="/login">
            Login
          </Button>
        )}
        {isLoggedIn && localStorage.getItem('role') === 'admin' && (
          <Button 
            color="inherit" 
            component={RouterLink} 
            to="/admin/tools" 
            startIcon={<BuildIcon />}
          >
            Manage Tools
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
