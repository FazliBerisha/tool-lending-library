import React from "react";
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Navbar from "./components/Navbar";

// Mock localStorage
const mockLocalStorage = () => {
  const storage = {};

  return {
    getItem: (key) => storage[key] || null,
    setItem: (key, value) => {
      storage[key] = value.toString();
    },
    removeItem: (key) => {
      delete storage[key];
    },
    clear: () => {
      for (let key in storage) {
        delete storage[key];
      }
    },
  };
};

global.localStorage = mockLocalStorage();

describe("Navbar Component", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renders the Reports button for admin users", () => {
    // Mock admin role
    localStorage.setItem("role", "admin");
    localStorage.setItem("token", "fake-token");

    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );

    // Assert Reports button is displayed
    const reportsButton = screen.getByText("Reports");
    expect(reportsButton).toBeInTheDocument();
    expect(reportsButton).toHaveAttribute("href", "/admin/reports");
  });

  it("does not render the Reports button for non-admin users", () => {
    // Mock non-admin role
    localStorage.setItem("role", "user");
    localStorage.setItem("token", "fake-token");

    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );

    // Assert Reports button is not displayed
    const reportsButton = screen.queryByText("Reports");
    expect(reportsButton).not.toBeInTheDocument();
  });

  it("does not render the Reports button for logged-out users", () => {
    // No token or role set in localStorage

    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );

    // Assert Reports button is not displayed
    const reportsButton = screen.queryByText("Reports");
    expect(reportsButton).not.toBeInTheDocument();
  });
});

global.localStorage = mockLocalStorage();

describe("Navbar Component", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("Renders the Reports button for admin users", () => {
    // Mock admin role
    localStorage.setItem("role", "admin");
    localStorage.setItem("token", "fake-token");

    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );

    // Assert Reports button is displayed
    const reportsButton = screen.getByText("Reports");
    expect(reportsButton).toBeInTheDocument();
    expect(reportsButton).toHaveAttribute("href", "/admin/reports");
  });

  it("Does not render the Reports button for non-admin users", () => {
    // Mock non-admin role
    localStorage.setItem("role", "user");
    localStorage.setItem("token", "fake-token");

    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );

    // Assert Reports button is not displayed
    const reportsButton = screen.queryByText("Reports");
    expect(reportsButton).not.toBeInTheDocument();
  });

  it("does not render the Reports button for logged-out users", () => {
    // No token or role set in localStorage

    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );

    // Assert Reviews button is not displayed
    const reportsButton = screen.queryByText("Reports");
    expect(reportsButton).not.toBeInTheDocument();
  });
});
