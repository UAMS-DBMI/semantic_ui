import React from 'react';
import { render } from '@testing-library/react';
import Beam from './Beam';

test('renders learn react link', () => {
  const { getByText } = render(<Beam />);
  const appTitle = getByText(/PRISM Beam/i);
  expect(appTitle).toBeInTheDocument();
});
