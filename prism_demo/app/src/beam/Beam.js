import React, {useState, useEffect, useCallback} from 'react';
import './Beam.css';
import REDCAP from './prism_datadictionary.json';
import RedcapFilter from './Redcapfilter';
import DataTable from './DataTable';


function TableRow(props){
  return (
    <tr className="filter_row" onClick={() => props.added(props.data.name)}>
      <td>{props.data.name}</td>
      <td>{props.data.label}</td>
    </tr>
  )
}

function FilterBox(props) {
  const [showBox, setShowBox] = useState(false);
  const [textFilter, setTextFilter] = useState("");

  const escFunction = useCallback((event) => {
    if(event.keyCode === 27) clear_all()
  }, []);

  useEffect(() => {
    document.addEventListener("keydown", escFunction, false);

    return () => {
      document.removeEventListener("keydown", escFunction, false);
    };
  }, [escFunction]);

  function added(name){
    setShowBox(false);
    setTextFilter("");
    props.added(name);
  }

  function clear_all(){
      setTextFilter("");
      setShowBox(false);
  }

  const filters = props.data.filter(row =>
    textFilter.length === 0 ||
    row.label.toLowerCase().indexOf(textFilter.toLowerCase()) >= 0
  ).map(row =>
    <TableRow data={row} key={row.name} added={added}/>
  );

  return (
    <div className="filter_div">
      <span className="filter_type">{props.must} Have</span>
      <div className="filter_container">
        <div className="filter_spreader">
          <div className="filter_search_box">
            <div className="filter_form">
              <input className="filter_search_input"
                     type="text"
                     value={textFilter}
                     onChange={(e) => {
                       setTextFilter(e.target.value);
                       setShowBox(true);
                     }}
                     placeholder="Search Term..."/>
              <svg className="filter_button" viewBox="0 0 490 490">
                <path fill="none" stroke="#000" strokeWidth="36" d="m280,278a153,153 0 1,0-2,2l170,170m-91-117 110,110-26,26-110-110"/>
              </svg>
            </div>
            <span className="explore_button" onClick={() => setShowBox(!showBox)}>
              <svg height="1em" width="1em" viewBox="0 0 512 512">
                <path d="m478.387 321.984h-28.847l-51.232-62.619c-6.409-7.836-15.892-12.33-26.016-12.33h-106.292v-57.02h94.969c18.534 0 33.613-15.079 33.613-33.613v-66.359c0-18.534-15.079-33.613-33.613-33.613h-60.565c-5.522 0-10 4.478-10 10s4.478 10 10 10h60.565c7.507 0 13.613 6.106 13.613 13.613v66.359c0 7.507-6.106 13.613-13.613 13.613h-209.938c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h60.666c5.522 0 10-4.478 10-10s-4.478-10-10-10h-60.666c-18.534 0-33.613 15.079-33.613 33.613v66.359c0 18.534 15.079 33.613 33.613 33.613h94.969v57.02h-106.697c-10.124 0-19.606 4.494-26.015 12.329l-51.233 62.62h-28.442c-18.534 0-33.613 15.079-33.613 33.614v66.359c0 18.534 15.079 33.613 33.613 33.613h66.359c18.534 0 33.613-15.079 33.613-33.613v-66.359c0-18.534-15.079-33.613-33.613-33.613h-12.077l40.873-49.957c2.596-3.173 6.436-4.992 10.535-4.992h106.697v54.949h-23.18c-18.534 0-33.613 15.079-33.613 33.613v66.359c0 18.534 15.079 33.613 33.613 33.613h66.359c18.534 0 33.613-15.079 33.613-33.613v-66.359c0-18.534-15.079-33.613-33.613-33.613h-23.179v-54.949h106.292c4.1 0 7.939 1.819 10.536 4.993l40.872 49.956h-11.673c-18.534 0-33.613 15.079-33.613 33.613v66.359c0 18.534 15.079 33.613 33.613 33.613h66.359c18.534 0 33.613-15.079 33.613-33.613v-66.359c.001-18.535-15.078-33.614-33.612-33.614zm-364.801 33.614v66.359c0 7.507-6.106 13.613-13.613 13.613h-66.36c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h66.359c7.507-.001 13.614 6.106 13.614 13.613zm189.207 0v66.359c0 7.507-6.106 13.613-13.613 13.613h-66.36c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h66.359c7.508-.001 13.614 6.106 13.614 13.613zm189.207 66.359c0 7.507-6.106 13.613-13.613 13.613h-66.359c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h66.359c7.507 0 13.613 6.106 13.613 13.613z"/>
                <path d="m246.77 70.25c2.067 5.039 8.028 7.494 13.05 5.41 5.03-2.087 7.501-8.014 5.41-13.051-2.091-5.036-8.012-7.509-13.06-5.42-5.024 2.079-7.488 8.045-5.4 13.061z"/>
              </svg>
            </span>
          </div>
          <div className="filter_results_container" style={{display: (showBox ? 'block' : 'none')}}>
            <button style={{float: 'right'}} onClick={() => clear_all()}>Close</button>
            <div className="filter_list">
              <table className="filter_table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {filters}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function Beam() {
  const [mustFilters, setMustFilters] = useState([]);
  const [cannotFilters, setCannotFilters] = useState([]);
  const [mustCohort, setMustCohort] = useState({});
  const [cannotCohort, setCannotCohort] = useState({});
  const [currentCohort, setCurrentCohort] = useState([]);
  const [showCohort, setShowCohort] = useState(false);
  const [allData, setAllData] = useState([]);
  const [cohortName, setCohortName] = useState("Unnamed");

  function reset_all(){
    setMustFilters([]);
    setCannotFilters([]);
    setMustCohort({});
    setCannotCohort({});
    setCurrentCohort([]);
    setShowCohort(false);
    setAllData([]);
    setCohortName("Unnamed");
  }

  function add_must_filter(name){
    let newFilters = mustFilters.slice();
    newFilters.push(name);
    setMustFilters(newFilters);
  }

  function remove_must_filter(name){
    let newFilters = mustFilters.filter((x) => x !== name);
    setMustFilters(newFilters);
    let newCohort = {...mustCohort};
    delete newCohort[name];
    setMustCohort(newCohort);
    update_current_cohort(newCohort, cannotCohort);
  }

  function add_cannot_filter(name){
    let newFilters = cannotFilters.slice();
    newFilters.push(name);
    setCannotFilters(newFilters);
  }

  function remove_cannot_filter(name){
    let newFilters = cannotFilters.filter((x) => x !== name);
    setCannotFilters(newFilters);
    let newCohort = {...cannotCohort};
    delete newCohort[name];
    setCannotCohort(newCohort);
    update_current_cohort(mustCohort, newCohort);
  }

  function get_data(name){
    for(let row of REDCAP){
      if(row.name === name){
        return row
      }
    }
  }

  function intersect(a, b) {
      return new Set([...a].filter(i => b.has(i)));
  }

  function update_current_cohort(mustCohort, cannotCohort){
    let mustSets = [];
    Object.keys(mustCohort).map((cohort) => mustSets.push(new Set(mustCohort[cohort])));
    var mustIntersection = new Set();
    if(Object.keys(mustCohort).length > 0){
      mustIntersection = mustSets.reduce(intersect);
    }
    var cannotArrays = [];
    for(var key in cannotCohort){
      cannotArrays = cannotArrays.concat(cannotCohort[key]);
    }
    let cannotUnion = new Set(cannotArrays);
    let finalCohort = Array.from(mustIntersection).filter(x => !cannotUnion.has(x));
    setCurrentCohort(finalCohort);
    fetch_all(finalCohort);
  }

  function add_must_cohort(name, patient_ids){
    let newMustCohort = {...mustCohort};
    newMustCohort[name] = patient_ids;
    setMustCohort(newMustCohort);
    update_current_cohort(newMustCohort, cannotCohort);
  }

  function add_cannot_cohort(name, patient_ids){
    let newCannotCohort = {...cannotCohort};
    newCannotCohort[name] = patient_ids;
    setCannotCohort(newCannotCohort);
    update_current_cohort(mustCohort, newCannotCohort);
  }

  async function fetch_all(currentCohort){
    let url = '/api/data?';
    let params = new URLSearchParams();
    params.set('patient_ids', currentCohort.join(','));
    const response = await fetch(url + params);
    let data = await response.json();
    setAllData(data);
  }

  let dUrl = '/api/data?';
  let dParams = new URLSearchParams();
  dParams.set('patient_ids', currentCohort.join(','));
  dParams.set('downloadFile', cohortName);
  const downloadLink = dUrl + dParams;

  const mustFilterBoxes = mustFilters.map(row =>
    <RedcapFilter data={get_data(row)} key={row} remove={remove_must_filter} fetch={add_must_cohort}/>
  );

  const cannotFilterBoxes = cannotFilters.map(row =>
    <RedcapFilter data={get_data(row)} key={row} remove={remove_cannot_filter} fetch={add_cannot_cohort}/>
  );

  let params = new URLSearchParams();
  params.set('PatientCriteria', currentCohort.join(','));
  const nbia_link = 'https://nbia.cancerimagingarchive.net/nbia-search/?' + params;

  return (
    <div>
      <header className="Beam-header">
        <div className="header_section" style={{flexGrow:1}}>
          <h2 className="collection_size header_title">Collection Size</h2>
          <span>1,082 subjects</span>
          <br/>
          <span>{REDCAP.length} data elements</span>
        </div>
        <div className="header_section" style={{flexGrow:3}}>
          <h2 className="header_title">Current Cohort - {currentCohort.length} subjects</h2>
          <div className="row_flex">
            <div style={{overflow: 'hidden'}}>
              <input className="cohort_name" value={cohortName} onChange={(e) => setCohortName(e.target.value)}/>
              <div style={{display: 'flex'}}>
                <button className="cohort_size_button" onClick={() => setShowCohort(!showCohort)}>
                  <svg className="filter_button" viewBox="0 0 490 490">
                    <path opacity="0.4" fill="none" stroke="#000" strokeWidth="36" d="m280,278a153,153 0 1,0-2,2l170,170m-91-117 110,110-26,26-110-110"/>
                  </svg>
                  <span>{showCohort ? "Hide" : "Show" } Subjects</span>
                </button>
                <a style={{textDecoration: 'none', width: '100%'}} href={downloadLink}>
                  <button className="cohort_size_button">
                    <svg version="1.1" viewBox="0 0 20 20" height="2em" with="2em">
                      <path
                        fill="#555753" opacity="0.5"
                        d="M.5 9.9a.5.5 0 01.5.5v2.5a1 1 0 001 1h12a1 1 0 001-1v-2.5a.5.5 0 011 0v2.5a2 2 0 01-2 2H2a2 2 0 01-2-2v-2.5a.5.5 0 01.5-.5z"
                      />
                      <path
                        fill="#555753" opacity="0.5"
                        d="M7.646 11.854a.5.5 0 00.708 0l3-3a.5.5 0 00-.708-.708L8.5 10.293V1.5a.5.5 0 00-1 0v8.793L5.354 8.146a.5.5 0 10-.708.708l3 3z"
                      />
                    </svg>
                    <span>Download CSV</span>
                  </button>
                </a>
              </div>
            </div>
            <button className="tallButton" onClick={() => reset_all()}>
              <svg version="1.1" viewBox="0 0 70 70" height="3em" with="3em">
                <g>
                  <g fill="#555753">
                    <path d="m32.5 4.999c-5.405 0-10.444 1.577-14.699 4.282l-5.75-5.75v16.11h16.11l-6.395-6.395c3.18-1.787 6.834-2.82 10.734-2.82 12.171 0 22.073 9.902 22.073 22.074 0 2.899-0.577 5.664-1.599 8.202l4.738 2.762c1.47-3.363 2.288-7.068 2.288-10.964 0-15.164-12.337-27.501-27.5-27.501z"/>
                    <path d="m43.227 51.746c-3.179 1.786-6.826 2.827-10.726 2.827-12.171 0-22.073-9.902-22.073-22.073 0-2.739 0.524-5.35 1.439-7.771l-4.731-2.851c-1.375 3.271-2.136 6.858-2.136 10.622 0 15.164 12.336 27.5 27.5 27.5 5.406 0 10.434-1.584 14.691-4.289l5.758 5.759v-16.112h-16.111l6.389 6.388z"/>
                  </g>
                </g>
              </svg>
              <span>New</span>
            </button>
            <a href={nbia_link} style={{textDecoration: 'none'}} target='_'>
              <button className="tallButton">
                <svg
                  fill="currentColor"
                  viewBox="0 0 16 16"
                  height="3em"
                  width="3em">
                  <path
                    fillRule="evenodd"
                    d="M.5 9.9a.5.5 0 01.5.5v2.5a1 1 0 001 1h12a1 1 0 001-1v-2.5a.5.5 0 011 0v2.5a2 2 0 01-2 2H2a2 2 0 01-2-2v-2.5a.5.5 0 01.5-.5z"
                  />
                  <path
                    fillRule="evenodd"
                    d="M7.646 11.854a.5.5 0 00.708 0l3-3a.5.5 0 00-.708-.708L8.5 10.293V1.5a.5.5 0 00-1 0v8.793L5.354 8.146a.5.5 0 10-.708.708l3 3z"
                  />
                </svg>
                <span>Browse Files</span>
              </button>
            </a>
          </div>
        </div>
      </header>
      {
        (showCohort === true)
        ? <div className="currentCohort">
            <DataTable data={allData} />
            <h2>All Patient Ids</h2>
            <p style={{width: '80%', wordWrap: 'break-word'}}>{currentCohort.join(',')}</p>
          </div>
        : <></>
      }
      <div className="filters">
        <div className="filter_item_container">
          <FilterBox must="MUST" data={REDCAP} added={add_must_filter}/>
          {mustFilterBoxes}
        </div>
        <div className="filter_item_container">
          <FilterBox must="CANNOT" data={REDCAP} added={add_cannot_filter}/>
          {cannotFilterBoxes}
        </div>
      </div>
    </div>
  );
}

export default Beam;
