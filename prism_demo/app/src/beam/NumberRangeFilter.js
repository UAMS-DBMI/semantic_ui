import React, {useState} from 'react';
import './Redcapfilter.css';

function NumberRangeFilter(props) {
  const [greaterThan, setGreaterThan] = useState("");
  const [lessThan, setLessThan] = useState("");
  const [data, setData] = useState(null);
  const [fetching, setFetching] = useState(null);

  async function fetchData(){
    setFetching(true);
    let url = '/api/age?';
    let params = new URLSearchParams();
    if(greaterThan !== "") params.set('min', greaterThan);
    if(lessThan !== "") params.set('max', lessThan);
    const response = await fetch(url + params);
    let data = await response.json();
    setData(data);
    setFetching(false);
    var cohort = [];
    for(var key in data){
      cohort = cohort.concat(data[key]);
    }
    props.fetch(props.data.name, cohort);
  }

  let summary = <></>;
  if(data !== null){
    let patient_count = 0;
    let distinct_count = 0;
    for(var age in data){
      distinct_count += 1;
      patient_count += data[age].length;
    }
    summary = <div>
      <p>Distinct Values: {distinct_count}</p>
      <p>Total Patients: {patient_count}</p>
    </div>
  }

  return (
    <div className="form_box">
      <button onClick={() => props.remove(props.data.name)}>X</button>
      <h4>{props.data.name}</h4>
      <p>{props.data.label}</p>
      <div className="boxes">
        <div className="num_boxes">
          <label>Greater than or equal to</label>
          <input type='number'
             value={greaterThan}
             onChange={(e) => {
               setGreaterThan(e.target.value);
             }}
             placeholder="Greater than..."/>
        </div>
        <div className="num_boxes">
          <label>Less than or equal to</label>
          <input type='number'
             value={lessThan}
             onChange={(e) => {
               setLessThan(e.target.value);
             }}
             placeholder="Less than..."/>
         </div>
      </div>
      <button onClick={fetchData} disabled={fetching}>Fetch Data</button>
      <div>{summary}</div>
    </div>
  );
}

export default NumberRangeFilter;
