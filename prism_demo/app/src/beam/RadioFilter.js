import React, {useState} from 'react';
import './Redcapfilter.css';
import './mybarchart.css';


function RadioFilter(props) {
  let startingFilters = {};
  for(let f of props.data.choices){
    startingFilters[f['value']] = {'enabled': false, 'label': f['label']};
  }
  const [filters, setFilters] = useState(startingFilters);
  const [data, setData] = useState(null);
  const [fetching, setFetching] = useState(null);
  const [disableButton, setDisableButton] = useState(true);
  const [allSelect, setAllSelect] = useState(false);

  async function fetchData(){
    setFetching(true);
    setDisableButton(true);
    let url = '/api/data/' + props.data.name + '?';
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
    setDisableButton(true);
    for(var key in newFilters){
      if(newFilters[key].enabled){
        setDisableButton(false);
      }
    }
    setFilters(newFilters);
  }

  function toggleAll(toggle){
    let newFilters = {...filters};
    for(var key in newFilters){
      newFilters[key].enabled = toggle;
    }
    setDisableButton(false);
    setAllSelect(toggle);
    setFilters(newFilters);
  }

  function check_boxes(choices){
    return Object.keys(choices).map((choice) =>
      <label key={choice} title={choice}>
        <input type='checkbox'
               onClick={(e) => modifyFilter(choice, e.target.checked)}
               readOnly checked={choices[choice].enabled}
               value={choice}/>
        {choices[choice].label}
      </label>
    );
  }

  function bar_boxes(choices, max){
    return Object.keys(choices).map((choice) =>
    <tr>
      <label key={choice} title={choice}>
        <input type='checkbox'
               onClick={(e) => modifyFilter(choice, e.target.checked)}
               readOnly checked={choices[choice].enabled}
               value={choice}/>
        {choices[choice].label}
      </label>
      {choice in data ?
      <td style={{'--size': 'calc(' + data[choice].length + '/' + max + ')'}}>
        {data[choice].length}
      </td>
      : <></>
      }
    </tr>
    );
  }

  let input = check_boxes(filters);

  let total_count = '';
  if(data !== null){
    let patient_count = 0;
    let max = 0;
    for(var key in data){
      let count = data[key].length;
      patient_count += count;
      if(count > max) max = count;
    }
    total_count = patient_count + ' total subjects';
    input = (<table className="my-charts-css bar reverse">
          <tbody>
            {bar_boxes(filters, max)}
          </tbody>
        </table>);
  }


  return (
    <div className="form_box">
      <button className="remove-button" onClick={() => props.remove(props.data.name)}>X</button>
      <h4>{props.data.name}</h4>
      <p>{props.data.label}</p>
      <div className="boxes">
        <input type='checkbox'
               style={{alignSelf: 'flex-start'}}
               onClick={() => toggleAll(!allSelect)}
               readOnly checked={allSelect}/>
        {input}
      </div>
      <div className="fetch-button">
        <button onClick={fetchData} disabled={disableButton}>Fetch Data</button>
        {fetching === true ? <span>...</span> : <></>}
        <span>{total_count}</span>
      </div>
    </div>
  );
}

export default RadioFilter;
