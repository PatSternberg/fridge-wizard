// file: frontend/src/App.test.js
import { BrowserRouter as Router } from 'react-router-dom';
import { render, screen } from '@testing-library/react';
import App from './App';

// Test that the app renders
test('renders the App component', () => {
  const { container } = render(
    <Router>
      <App />
    </Router>
  );
  expect(container).toBeInTheDocument();
});