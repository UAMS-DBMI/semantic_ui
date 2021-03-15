import React from 'react';
import { render, screen } from '@testing-library/react';
import RedcapFilter from './RedcapFilter';

test('renders a form element', () => {
  render(<RedcapFilter />);
  const formElement = document.querySelector('form');
  expect(formElement).toBeInTheDocument();
});

test('renders the description', () => {
  const test_data =   {
      "form_name": "test",
      "type": "text",
      "name": "test",
      "label": "TEST LABEL"
    };
  render(<RedcapFilter data={test_data} />);
  const label = screen.queryByText('TEST LABEL');
  expect(label).toBeInTheDocument();
});

test('renders a text input for text fields', () => {
  const test_data =   {
      "form_name": "test",
      "type": "text",
      "name": "test",
      "label": "test"
    };
  render(<RedcapFilter data={test_data} />);
  const textInput = screen.queryByRole('textbox');
  expect(textInput).toBeInTheDocument();
});

test('renders a calc input with number field', () => {
  const test_data =   {
      "form_name": "test",
      "type": "calc",
      "name": "test",
      "label": "test"
    };
  render(<RedcapFilter data={test_data} />);
  const numberInput = document.querySelector('input[type="number"]');
  expect(numberInput).toBeInTheDocument();
});

test('renders options for radio', () => {
  const test_data = {
    "form_name": "test",
    "choices": [
      {
        "value": "0",
        "label": "Male"
      },
      {
        "value": "1",
        "label": "Female"
      },
      {
        "value": "2",
        "label": "Other"
      }
    ],
    "type": "radio",
    "name": "gender",
    "label": "Gender"
  };
  render(<RedcapFilter data={test_data} />);
  const male = screen.getByLabelText('Male');
  expect(male).toBeInTheDocument();
  const female = screen.getByLabelText('Female');
  expect(female).toBeInTheDocument();
  const other = screen.getByLabelText('Other');
  expect(other).toBeInTheDocument();
});
