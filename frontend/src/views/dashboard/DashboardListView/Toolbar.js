import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import {
  Box,
  // Button,
  Card,
  CardContent,
  makeStyles,
  CardHeader,
  Divider,
  Grid
} from '@material-ui/core';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';


const useStyles = makeStyles((theme) => ({
  root: {},
  importButton: {
    marginRight: theme.spacing(1)
  },
  exportButton: {
    marginRight: theme.spacing(1)
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 180,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

const Toolbar = ({ className, ...rest }) => {
  const classes = useStyles();
  const [client, setClient] = React.useState('All');
  const [project, setProject] = React.useState('All');
  const [st, setSt] = React.useState('All');
  const [requestor, setRequestor] = React.useState('All');

  const handleChangeClient = (event) => {
    setClient(event.target.value);
  };
  const handleChangeProject = (event) => {
    setProject(event.target.value);
  };
  const handleChangeSt = (event) => {
    setSt(event.target.value);
  };
  const handleChangeRequestor = (event) => {
    setRequestor(event.target.value);
  };

  return (
    <div
      className={clsx(classes.root, className)}
      {...rest}
    >
   
      <Grid>

      <Box mt={3}>
        <Card >
        <CardHeader align='center' title="PROJECT DETAILS" />
         <Divider />
        <CardContent>
            <Box
              display="flex"
              justifyContent="space-between"
            >
            
       <FormControl className={classes.formControl}>
        <InputLabel id="demo-simple-select-label">Client</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={client}
          onChange={handleChangeClient}
        >
          <MenuItem value={'All'}>All</MenuItem>
     
        </Select>
      </FormControl>
      <FormControl className={classes.formControl}>
        <InputLabel id="demo-simple-select-label">Project Name</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={project}
          onChange={handleChangeProject}
        >
          <MenuItem value={'All'}>All</MenuItem>
     
        </Select>
      </FormControl>
      <FormControl className={classes.formControl}>
        <InputLabel id="demo-simple-select-label">ST</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={st}
          onChange={handleChangeSt}
        >
          <MenuItem value={'All'}>All</MenuItem>
          
        </Select>
      </FormControl>
      <FormControl className={classes.formControl}>
        <InputLabel id="demo-simple-select-label">Requestor</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={requestor}
          onChange={handleChangeRequestor}
        >
          <MenuItem value={'All'}>All</MenuItem>
          
        </Select>
      </FormControl>
   
            </Box>
          </CardContent> 
        </Card>
      </Box>
      </Grid>
      </div>
  );
};

Toolbar.propTypes = {
  className: PropTypes.string
};

export default Toolbar;
