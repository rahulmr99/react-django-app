import React from 'react';
import clsx from 'clsx';
// import { Doughnut } from 'react-chartjs-2';
import {
  // Box,
  Card,
  CardContent,
  // CardHeader,
  // Divider,
  // Typography,
  // colors,
  makeStyles,
  // useTheme
} from '@material-ui/core';


// /static/images/avatars/avatar_1.png'

const useStyles = makeStyles(() => ({
  root: {
    height: '70%',
  width:"100%"  }
}));

const ProjectImage = ({ className, ...rest }) => {
  const classes = useStyles();


  return (
    <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      {/* <CardHeader title="Traffic by Device" /> */}
      {/* <Divider /> */}
      <CardContent>
        {/* <img src={imgUrl} alt="Project Overview"/> */}
        <div style={{textAlign:"center"}}>
        <img src={localStorage.getItem("imgaddress")} alt="Project Overview"/>

        </div>
        

     
      </CardContent>
    </Card>
  );
};



export default ProjectImage;
