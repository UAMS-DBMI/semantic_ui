import React, {useState} from 'react';
import './Redcapfilter.css';


function RadioFilter(props) {
  let startingFilters = {};
  for(let f of props.data.choices){
    startingFilters[f['value']] = {'enabled': false, 'label': f['label']};
  }
  const [filters, setFilters] = useState(startingFilters);
  const [data, setData] = useState(null);
  const [fetching, setFetching] = useState(null);

  async function fetchData(){
    setFetching(true);
    let url = 'http://localhost:3000/data/' + props.data.name + '?';
    let params = new URLSearchParams();
    let uris = Object.keys(filters).filter((uri) =>
      filters[uri].enabled
    )
    params.set('uris', uris.join(','));
    const response = await fetch(url + params);
    setFetching(false);
    let data = await response.json();
    setData(data);
    var cohort = [];
    for(var key in data){
      cohort = cohort.concat(data[key]);
    }
    props.fetch(props.data.name, cohort);
  }

  function modifyFilter(choice, checked){
    let newFilters = {...filters};
    newFilters[choice].enabled = checked;
    setFilters(newFilters);
  }

  function check_boxes(choices){
    return Object.keys(choices).map((choice) =>
      <label key={choice}>
        <input type='checkbox'
               onClick={(e) => modifyFilter(choice, e.target.checked)}
               readOnly checked={choices[choice].enabled}
               value={choice}/>
        {choices[choice].label}
      </label>
    );
  }

  let summary = <></>;
  if(data !== null){
    let patient_count = 0;
    let distinct_count = 0;
    for(var key in data){
      distinct_count += 1;
      patient_count += data[key].length;
    }
    summary = <div>
      <p>Distinct Values: {distinct_count}</p>
      <p>Total Patients: {patient_count}</p>
    </div>
  }

  let input = check_boxes(filters);

  return (
    <div className="form_box">
      <button onClick={() => props.remove(props.data.name)}>X</button>
      <h4>{props.data.name}</h4>
      <p>{props.data.label}</p>
      <div className="boxes">
        {input}
      </div>
      <button onClick={fetchData} disabled={fetching}>Fetch Data</button>
      <div>{summary}</div>
    </div>
  );
}

export default RadioFilter;
