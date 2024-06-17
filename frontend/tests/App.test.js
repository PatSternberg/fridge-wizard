import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../src/App';

// Test that the App component renders the Home component by default
test('renders Home component by default', () => {
  render(
    <MemoryRouter initialEntries={['/']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Become a')).toBeInTheDocument(); // Update with actual text/content of Home component
});

// Test that the App component renders the Fridge component when navigating to /fridge
test('renders Fridge component for /fridge route', () => {
  render(
    <MemoryRouter initialEntries={['/fridge']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('My fridge')).toBeInTheDocument(); // Update with actual text/content of Fridge component
});

// Test that the App component renders the Recipes component when navigating to /recipes
test('renders Recipes component for /recipes route', () => {
  render(
    <MemoryRouter initialEntries={['/recipes']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('My recipes')).toBeInTheDocument(); // Update with actual text/content of Recipes component
});

// Test that the App component renders the Profile component when navigating to /profile
test('renders Profile component for /profile route', () => {
  render(
    <MemoryRouter initialEntries={['/profile']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Loading user profile...')).toBeInTheDocument(); // Update with actual text/content of Profile component
});
