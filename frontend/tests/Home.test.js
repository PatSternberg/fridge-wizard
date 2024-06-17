// file: frontend/tests/Home.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Home from '../src/pages/Home';

describe('Home Component', () => {
    const renderWithRouter = (ui, { route = '/' } = {}) => {
        return render(
            <MemoryRouter initialEntries={[route]}>
            {ui}
            </MemoryRouter>
        );
    };

  test('renders Welcome component by default', () => {
    renderWithRouter(<Home />);
    expect(screen.getByText(/Become a/i)).toBeInTheDocument();
  });

  test('renders SignUp component on SignUp button click', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByTestId('signup-button'));
    expect(screen.getByTestId('signup-button')).toBeInTheDocument();
  });

  test('renders LogIn component on LogIn button click', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByTestId('login-button'));
    expect(screen.getByTestId('login-button')).toBeInTheDocument();
  });

    // To add test for testing back button on signup and login pages
});
