import * as React from 'react';
import { TextField } from '@mui/material';
import { Controller } from 'react-hook-form';

export default function MyTextField(props) {
  const {label, name, control} = props
  return (
      <Controller
        name = {name}
        control = {control}
        render = {({
          field: {onChange, value},
          fieldState: {error},
          formState,
      }) => (
          <TextField
            id="standard-basic"
            label={label}
            onChange={onChange}
            value={value}
            variant="standard" />
      )}
      />
  );
}