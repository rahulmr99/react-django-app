import React, { useEffect, useState } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import {
  Avatar,
  Box,
  // Button,
  Divider,
  Drawer,
  Hidden,
  List,
  Typography,
  makeStyles
} from '@material-ui/core';
import {
  // AlertCircle as AlertCircleIcon,
  BarChart as BarChartIcon,
  // Lock as LockIcon,
  // Settings as SettingsIcon,
  // ShoppingBag as ShoppingBagIcon,
  // User as UserIcon,
  // UserPlus as UserPlusIcon,
  // Users as UsersIcon,
  Upload as Project
  // ArrowUpCircle as Project
} from 'react-feather';
import NavItem from './NavItem';

const user = {
  // avatar: '/static/images/avatars/avatar_6.png',
  // jobTitle: 'Senior Developer'
  // name: 'Rooftop '
};


let items = [
  {
    href: '/app/dashboard',
    icon: BarChartIcon,
    title: 'Dashboard'
  },
 
  {
    href: '/app/addProject',
    icon: Project,
    title: 'Add Project'
  },
 
  // {
  //   href: '/app/register',
  //   icon: UserPlusIcon,
  //   title: 'Add New Employee'
  // },
  // {
  //   href: '/login',
  //   icon: LockIcon,
  //   title: 'Logout'
  // },
  //   {
  //   href: '/app/products',
  //   icon: ShoppingBagIcon,
  //   title: 'Products'
  // },
 
];

let employeeItems = [

  {
    href: '/app/dashboard',
    icon: BarChartIcon,
    title: 'Dashboard'
  },

  {
    href: '/app/addProject',
    icon: Project,
    title: 'Add Project'
  },

  // {
  //   href: '/login',
  //   icon: LockIcon,
  //   title: 'Logout'
  // }
]



const useStyles = makeStyles(() => ({
  mobileDrawer: {
    width: 256
  },
  desktopDrawer: {
    width: 256,
    top: 64,
    height: 'calc(100% - 64px)'
  },
  avatar: {
    cursor: 'pointer',
    width: 64,
    height: 64
  }
}));

const NavBar = ({ onMobileClose, openMobile }) => {
  const classes = useStyles();
  const location = useLocation();

  const [navItems, setNavItems] = useState(items)


  useEffect(() => {
    if (openMobile && onMobileClose) {
      onMobileClose();
    }


    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname]);

  useEffect(() => {
    if (localStorage.getItem('userType') === '1') {
      setNavItems(items)
    } else {

      setNavItems(employeeItems)
    }

  }, [])

  const content = (
    <Box
      height="100%"
      display="flex"
      flexDirection="column"
    >
      <Box
        alignItems="center"
        display="flex"
        flexDirection="column"
        p={2}
      >
        <Avatar
          className={classes.avatar}
          component={RouterLink}
          src={user.avatar}
          to="/app/dashboard"
        />
        <Typography
          className={classes.name}
          color="textPrimary"
          variant="body2"
          p={2}
        >
          {localStorage.getItem('userName')}
        </Typography>
        {/* <Typography
          color="textSecondary"
          variant="body2"
        >
     
        {user.jobTitle} 
        </Typography> */}
      </Box>
      <Divider />
      <Box p={2}>
        <List>
          {navItems.map((item) => (
            <NavItem
              href={item.href}
              key={item.title}
              title={item.title}
              icon={item.icon}
            />
          ))}
        </List>
      </Box>
      <Box flexGrow={1} />
      <Box
        p={2}
        m={2}
        bgcolor="background.dark"
      >
        {/* <Typography
          align="center"
          gutterBottom
          variant="h4"
        >
          Need more?
        </Typography>
        <Typography
          align="center"
          variant="body2"
        >
          Upgrade to PRO version and access 20 more screens
        </Typography> */}
        <Box
          display="flex"
          justifyContent="center"
          mt={2}
        >
          {/* <Button
            color="primary"
            component="a"
            href="https://react-material-kit.devias.io"
            variant="contained"
          >
            See PRO version
          </Button> */}
        </Box>
      </Box>
    </Box>
  );

  return (
    <>
      <Hidden lgUp>
        <Drawer
          anchor="left"
          classes={{ paper: classes.mobileDrawer }}
          onClose={onMobileClose}
          open={openMobile}
          variant="temporary"
        >
          {content}
        </Drawer>
      </Hidden>
      <Hidden mdDown>
        <Drawer
          anchor="left"
          classes={{ paper: classes.desktopDrawer }}
          open
          variant="persistent"
        >
          {content}
        </Drawer>
      </Hidden>
    </>
  );
};

NavBar.propTypes = {
  onMobileClose: PropTypes.func,
  openMobile: PropTypes.bool
};

NavBar.defaultProps = {
  onMobileClose: () => { },
  openMobile: false
};

export default NavBar;
