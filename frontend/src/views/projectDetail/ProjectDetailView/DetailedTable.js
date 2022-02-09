import React, { useState, forwardRef ,useEffect} from "react";
import clsx from 'clsx';
import { connect } from 'react-redux';
import {
  Card,
  CardHeader,
  Divider,
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import MaterialTable from "material-table";
import AddBox from '@material-ui/icons/AddBox';
// import ArrowDownward from '@material-ui/icons/ArrowDownward';
import Check from '@material-ui/icons/Check';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
// import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';

import * as actionCreators from '../../../store/actions/userDataAction';



const useStyles = makeStyles(() => ({
  root: {},
  actions: {
    justifyContent: 'flex-end'
  }
}));

const DetailTable = (props,{ className, ...rest }) => {
  const classes = useStyles();
  // const [orders] = useState(data);
  const [dataCost,setDataCost] = useState([props.detailedInfo])
  const [dataFinance,setDataFinance] = useState([props.detailedInfo])
  const [dataEng,setDataEng] = useState([props.detailedInfo])
  const [dataIncentives,setDataIncentives] = useState([props.detailedInfo])

  useEffect(()=>{
    console.log(localStorage.getItem("projectId"))
    const id = localStorage.getItem("projectId")
    props.OnDetailedProject(id);
    },[ ])

    useEffect(()=>{
      setDataCost([props.detailedInfo])
      setDataFinance([props.detailedInfo])
      setDataEng([props.detailedInfo])
      setDataIncentives([props.detailedInfo])
    },[props.detailedInfo ])
         
    
    const [columnsFinance, setColumnsFinance] = useState([
      { title: 'Project Name',field: 'project_name',sorting:false},
      { title: 'Efficient IRR', field: 'effIrr',sorting:false}, 
      { title: ' ST', field: 'st' ,sorting:false, cellStyle: {padding: "10px"},},
      { title: 'Utility Rate[$/W]', field: 'utilityRate',sorting:false },
      // { title: 'Specific Production[kWh/kWp]', field: 'specificProd',sorting:false },
      { title: 'Prospector Specific Production[kWh/kW/yr]', field: 'calculations[0].prospector_specific_production',sorting:false,emptyValue:" ", 
      render: rowData => rowData.calculations[0].prospector_specific_production.toFixed(2)},
      { title:  'Build Cost[$/W]', field: 'buildCost' ,sorting:false}, 
    ]);

  const [columnsCost, setColumnsCost] = useState([
    { title: ' Build Cost[$/W]', field: 'buildcost', sorting:false },
    { title: 'Labor Cost[$/W]', field: 'calculations[0].labor_cost_per_watt',sorting:false,emptyValue:" ",
    //  render: rowData =>  rowData.calculations[0].labor_cost_per_watt.toFixed(2)
     },
     { title: 'Module Cost[$/W]]', field: 'calculations[0].module_cost_per_watt',sorting:false,emptyValue:" ",
    //  render: rowData =>  rowData.calculations[0].module_cost_per_watt.toFixed(2) 
    },
    { title: 'Inverter [$/W]', field: 'inverter',sorting:false },
    { title:  'Optimizer [$/W]', field: 'Optimizer',sorting:false }, 
    { title: 'BOS[$/W]', field: 'BOS',sorting:false },
    { title: 'O&M[$/W]', field: 'OM',sorting:false },
  ]);

  const [columnsEng, setColumnsEng] = useState([

    { title: 'Estimated DC[kW]', field: 'calculations[0].estimated_dc_size',sorting:false,emptyValue:" ",
    render: rowData =>  rowData.calculations[0].estimated_dc_size.toFixed(2)},
    { title: 'Estimated AC[kW]', field: 'calculations[0].estimated_ac_size',sorting:false,emptyValue:" ",
    render: rowData =>  rowData.calculations[0].estimated_ac_size.toFixed(2) },
    { title: 'Prospector Specific Production[kWh/kW/yr]', field: 'calculations[0].prospector_specific_production',sorting:false,emptyValue:" ", 
      render: rowData => rowData.calculations[0].prospector_specific_production.toFixed(2)},
    { title: 'Number of Modules', field: 'modules',sorting:false },
    { title:  'Number of Optimizers', field: 'optimizer',sorting:false }, 
    { title: 'Azimuth', field: 'azimuth' ,sorting:false}
  ]);



  const [columnsIncentives, setColumnsIncentives] = useState([
    { title: ' Program', field: 'program', sorting:false },
    { title: 'Type', field: 'type',sorting:false},
    { title: 'Metering', field: 'metering',sorting:false },
    { title: 'SizeFloor [kW AC]', field: 'sizeFloor',sorting:false, cellStyle: {minWidth: 50} },
    { title:  'SizeCap [kW AC]', field: 'sizeCap',sorting:false }, 
    { title: 'Effective Year1($/kWh)', field: 'effectiveYear',sorting:false }
  ]);

  // const [dataFinance, setDataFinance] = useState([
  //   { project: 'SpeederTech		', effIrr: '12.87%', st: ' NJ',specificProd: ' 1511.27',utilityRate:'$ 0.11 ', buildCost: '$ 0.11	'},
  // ]);

  // const [dataCost, setDataCost] = useState([
  //   { buildcost: '$ 1.77', Labour: '$ 0.72', Module: ' $ 0.43',inverter:'$ 0.04', BOS: '$ 0.09', Optimizer: '$ 0.49', OM: '$ 15.00' },
  // ]);

  // const [dataEng, setDataEng] = useState([
  //   { edc: '966.07	', eac: '	720.00', specificProd: ' 1511.27',modules:'2611.00', optimizer: '1305	', azimuth: '215'},
  // ]);

  // const [dataIncentives, setDataIncentives] = useState([
  //   { program: 'NJ TREC', type: ' ', metering: ' NEM',sizeFloor:' 25.00', sizeCap: '10000', effectiveYear: '$ 0.065' },
  // ]);


  const tableIcons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  // Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  // Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
  // Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  // FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  // LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  // NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  // PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
  // ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  // Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  // SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
  // ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  // ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />)
    };


  return (
    <Container maxWidth={false}>
    <Grid
      container
      spacing={3}
    >
      <Grid
        item
        xs={12}
      >
   <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <CardHeader align='center' title="PROJECT FINANCE" />
      <Divider />
      <MaterialTable
      options={{
        search: false,
        paging: false,
        toolbar:false
      }}
        icons ={tableIcons}
        columns={columnsFinance}
        data={dataFinance}
        editable={{
          onRowUpdate: (newData, oldData) =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                // const dataUpdate = [...dataFinance];
                // const index = oldData.tableData.id;
                // dataUpdate[index] = newData;
                // setDataFinance([...dataUpdate]);
                resolve();
              }, 100)
            }),
        }}
      />
    </Card>
      </Grid>
      <Grid
        item
   
        xs={12}
      >
        <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <CardHeader align='center' title="ENGINEERING" />
      <Divider />
      <MaterialTable
      options={{
        search: false,
        paging: false,
        toolbar:false
      }}
        icons ={tableIcons}
        columns={columnsEng}
        data={dataEng}
        editable={{
          onRowUpdate: (newData, oldData) =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                // const dataUpdate = [...dataEng];
                // const index = oldData.tableData.id;
                // dataUpdate[index] = newData;
                // setDataEng([...dataUpdate]);
                resolve();
              }, 50)
            }),
        }}
      />
    </Card>
      </Grid>
      <Grid item xs={12}>
      <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <CardHeader align='center' title="COST" />
      <Divider />
        {/* <EditTableDemo/> */}
        <MaterialTable
      options={{
        search: false,
        paging: false,
        toolbar:false
      }}
        icons ={tableIcons}
        columns={columnsCost}
        data={dataCost}
        editable={{
          onRowUpdate: (newData, oldData) =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                // const dataUpdate = [...dataCost];
                // const index = oldData.tableData.id;
                // dataUpdate[index] = newData;
                // setDataCost([...dataUpdate]);
                resolve();
              }, 50)
            }),
        }}
      />
        </Card>
        </Grid>
        <Grid item xs={12}>
      <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <CardHeader align='center' title="INCENTIVES" />
      <Divider />
        {/* <EditTableDemo/> */}
        <MaterialTable
      options={{
        search: false,
        paging: false,
        toolbar:false
      }}
        icons ={tableIcons}
        columns={columnsIncentives}
        data={dataIncentives}
        editable={{
          onRowUpdate: (newData, oldData) =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                // const dataUpdate = [...dataIncentives];
                // const index = oldData.tableData.id;
                // dataUpdate[index] = newData;
                // setDataIncentives([...dataUpdate]);
                resolve();
              }, 50)
            }),
        }}
      />
        </Card>
        </Grid>
    </Grid>
  </Container>
   
  );
};


const mapStateToProps = state => {
  return{
    detailedInfo:state.user.detailedProjectInfo,
    isLoading:state.user.isLoading
  }
}
const mapDisptachToProps = dispatch =>{
  return {
    OnDetailedProject : (payload,callback) => dispatch(actionCreators.detailedProject(payload,callback))
  }
}
export default (connect(mapStateToProps,mapDisptachToProps)(DetailTable))



