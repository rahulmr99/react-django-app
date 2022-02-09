import React, {  useEffect ,useState,forwardRef} from 'react';
import clsx from 'clsx';
import { connect } from 'react-redux';
import Modal from '../../../utils/ui/Modal';
import { useNavigate } from 'react-router-dom';
import * as actionCreators from '../../../store/actions/userDataAction';
import {
  Card,
  Button,
  makeStyles,
  Link
} from '@material-ui/core';
import MaterialTable from "material-table";
import AddBox from '@material-ui/icons/AddBox';
// import ArrowDownward from '@material-ui/icons/ArrowDownward';
import Check from '@material-ui/icons/Check';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
// import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';

const useStyles = makeStyles((theme) => ({
  root: {},
  avatar: {
    marginRight: theme.spacing(2)
  }
}));

const Results = (props,{ className, customers, ...rest }) => {
  const classes = useStyles();
  const navigate = useNavigate();

 

  
  const [columnsTable, setColumnsTable] = useState([
    { title: 'Client', field: 'client', sorting:false },
    { title: 'Project Name',field: 'project_name',sorting:false,
      render: rowData => 
        <Link
        component="button"
        variant="body2"
        onClick={()=>rowtableHandler(rowData)}
      >
        {rowData.project_name}
      </Link>
    },
    { title: 'Building Type', field: 'building_type',sorting:false },
    { title: 'Task Target', field: 'task_target',sorting:false },
    { title:  'Consumption Overwrite', field: 'consumption_overwrite',sorting:false }, 
    { title: 'Utility Overwrite', field: 'utility_overwrite',sorting:false },
    // { title: 'Efficient IRR', field: 'effIr',sorting:false,emptyValue:" " },
    // { title: 'Incentive Program', field: 'incentiveProgram',sorting:false,emptyValue:"SmartFit-Block3" },
    { title: 'Equipment Cost [$/W]',field: 'calculations[0].equipment_cost_per_watt',sorting:false,emptyValue:" " ,
      render: rowData =>  rowData.calculations[0].equipment_cost_per_watt.toFixed(2)
    },
    { title: 'Estimated Consumption [kWh]',field: 'calculations[0].estimated_consumption',sorting:false,emptyValue:" ",
      render: rowData =>  rowData.calculations[0].estimated_consumption.toFixed(2)
    },
    { title: 'Estimated AC[kW]', field: 'calculations[0].estimated_ac_size',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].estimated_ac_size.toFixed(2) },
    { title: 'Estimated DC[kW]', field: 'calculations[0].estimated_dc_size',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].estimated_dc_size.toFixed(2)},
    { title: 'Estimated Modules', field: 'calculations[0].estimated_modules',sorting:false,emptyValue:" " },
    { title: 'Inverter Manufacturer', field: 'calculations[0].inverter_manufacturer',sorting:false,emptyValue:" " },
    { title: 'Inverter Total Cost[USD]', field: 'calculations[0].inverter_total_cost',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].inverter_total_cost.toFixed(2)},
    { title: 'Labor Cost[$/W]', field: 'calculations[0].labor_cost_per_watt',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].labor_cost_per_watt.toFixed(2) },
    { title: 'Module Cost[$/W]]', field: 'calculations[0].module_cost_per_watt',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].module_cost_per_watt.toFixed(2) },
    { title: 'Module Degradation[%/yr]', field: 'calculations[0].module_degradation_per_year',sorting:false,emptyValue:" " },
    { title: 'Module Manufacturer', field: 'calculations[0].module_manufacturer',sorting:false,emptyValue:" " },
    { title: 'Module Size', field: 'calculations[0].module_size',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].module_size.toFixed(2) },
    { title: 'Module Total Cost[USD]', field: 'calculations[0].module_total_cost',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].module_total_cost.toFixed(2)},
    { title: 'Optimizer Total Cost[USD]', field: 'calculations[0].optimizer_total_cost',sorting:false,emptyValue:" ",
     render: rowData =>  rowData.calculations[0].optimizer_total_cost.toFixed(2)},
    { title: 'Optimizer Unitary Cost[USD]', field: 'calculations[0].optimizer_unitary_cost',sorting:false,emptyValue:" ",
    render: rowData =>  rowData.calculations[0].optimizer_unitary_cost.toFixed(2)},
    { title: 'Prospector Specific Production[kWh/kW/yr]', field: 'calculations[0].prospector_specific_production',sorting:false,emptyValue:" ", 
    render: rowData => rowData.calculations[0].prospector_specific_production.toFixed(2)},
    { title: 'Target Modules', field: 'calculations[0].target_modules',sorting:false,emptyValue:" " },
    { title: 'Target Size[kW]', field: 'calculations[0].target_size',sorting:false,emptyValue:" ",
    render: rowData => rowData.calculations[0].target_size.toFixed(2)},
    { title: 'TMY3 Specific Production[kWh/kW/yr]', field: 'calculations[0].tmy3_specific_production',sorting:false,emptyValue:" ",
    render: rowData => rowData.calculations[0].tmy3_specific_production.toFixed(2)},
    { title: 'Total Cost[$/W]', field: 'calculations[0].total_cost_per_watt',sorting:false,emptyValue:"$ 2.25",
    render: rowData => rowData.calculations[0].total_cost_per_watt.toFixed(2)},
    { title: 'Total Cost[USD]', field: 'calculations[0].total_cost',sorting:false,emptyValue:"$ 2.25",
    render: rowData => rowData.calculations[0].total_cost.toFixed(2)},
    {
      title: 'Image url',
      field: 'address_image',
      render: rowData => 
         <Button
          variant="outlined" color="primary" size="small"
          onClick= { ()=> handleImage(rowData.address_image)
          }
        >
          <span style={{ textTransform: "lowercase"}}>  View Image</span>
        </Button>
    }
  ]);

  // const [dataAddress,setDataAddress]= useState(props.addressList)
  const[imgUrl,setImgUrl] = useState(null);
  const[trigger,setTrigger] = useState(false);

  useEffect(()=>{
  localStorage.setItem('accessToken', `${process.env.REACT_APP_ACCESS_TOKEN}`);
  props.OnAddressDetails();
  },[ ])

  // useEffect(()=>{
  //   setDataAddress(props.addressList)
  //   },[props.addressList])


  const handleImage = (imageUrl) => {
    setImgUrl(imageUrl?imageUrl:'/static/images/noimage.jpg')
    setTrigger(prevState => ({
      trigger: !prevState.trigger
    }));
  }

  const rowtableHandler = (row) => {
    console.log("inside row table hanlder",row);
    localStorage.setItem("projectId",row.id)
    if(row.address_image)
    {
      localStorage.setItem("imgaddress",row.address_image)
    }
    else{
      localStorage.setItem("imgaddress","/static/images/no-image.jpg")
    }
    navigate('/app/projectOverview');
  }

  const tableIcons = {
    Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
    Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
    Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
    Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  };
  

  return (
    <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
     <MaterialTable
      options={{
        search: false,
        paging: false,
        toolbar:false
      }}
     
        icons ={tableIcons}
        columns={columnsTable}
        data={props.addressList}
        // data={dataAddress}
        // editable={{
        //   onRowUpdate: (newData, oldData) =>
        //     new Promise((resolve, reject) => {
        //       setTimeout(() => {
        //         const dataUpdate = [...dataAddress];
        //         const index = oldData.tableData.id;
        //         dataUpdate[index] = newData;
        //         setDataAddress([...dataUpdate]);
        //         resolve();
        //       }, 100)
        //     }),
        // }}
      />
       {imgUrl? <> <Modal imgUrl={imgUrl} trigger={trigger}/> </>: null} 
    </Card>
  );
};



const mapStateToProps = state => {
  // console.log("state in  profile details",state)
  return{
      userInfo: state.user.userInfo,
      loginInfo:state.log.loginDetails,
      addressList:state.user.addressList,
      isLoading:state.user.isLoading

  }
}
const mapDisptachToProps = dispatch =>{
  return {
      OnAddressDetails : (payload,callback) => dispatch(actionCreators.addressDetails(payload,callback))
     
  }
}
export default (connect(mapStateToProps,mapDisptachToProps)(Results));

