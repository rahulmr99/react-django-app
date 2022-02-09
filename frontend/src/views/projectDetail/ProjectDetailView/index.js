import React from 'react';
import {
  Box,
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
// import { Pagination } from '@material-ui/lab';
import Page from 'src/components/Page';
// import Toolbar from './Toolbar';
import LatestOrders from './DetailedTable';
import ProjectImage from './ProjectImage';
// import ProductCard from './ProductCard';
// import data from './data';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3),
    position:'absolute'
  },
  productCard: {
    height: '100%'
  }
}));

const ProductList = () => {
  const classes = useStyles();
  // const [products] = useState(data);

  return (
    <Page
      className={classes.root}
      // title="Products"
    >
      <Container >
        {/* <Toolbar /> */}
        <Box mt={3}>
          <Grid
            container
            spacing={1}
          >
           
              <Grid
                item
                lg={6}
                md={6}
                xs={12}
              >
                  <LatestOrders/>
              </Grid>
            
              <Grid
                item
                lg={6}
                md={6}
                xs={12}
              >
                    <ProjectImage/> 
              </Grid>

          </Grid>
        </Box>
      </Container>
    </Page>
  );
};

export default ProductList;
