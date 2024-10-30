import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import UserProfile from './components/UserProfile';
import BrowseTools from './components/BrowseTools';
import AdminToolsPanel from './components/AdminToolsPanel';
import ProtectedRoute from './components/ProtectedRoute';
import ReservationPanel from './components/ReservationPanel';

const theme = createTheme({
  palette: {
    primary: {
      main: '#4caf50', // Green
    },
    secondary: {
      main: '#ffc107', // Yellow/Orange
    },
    background: {
      default: '#f5f5f5', // Light grey background
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/browse" element={<BrowseTools />} />
          <Route 
            path="/admin/tools" 
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AdminToolsPanel />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/reservations" 
            element={
              <ProtectedRoute>
                <ReservationPanel />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
