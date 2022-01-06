import React, {useState, useEffect, useCallback} from 'react';
import './Beam.css';
import RedcapFilter from './Redcapfilter';
import DataTable from './DataTable';
import { useFetch } from './useFetch';
import DataLogo from './data_logo.svg';
import FilesLogo from './files_logo.svg';
import PersonLogo from './person_logo.svg';

function CategoryTableRow(props){
  return (
    <tr className="filter_row" onClick={() => props.added(props.data.name, null)}>
      <td>{props.data.name}</td>
      <td>{props.data.label}</td>
    </tr>
  )
}

function TermTableRow(props){
  return (
    <tr className="filter_row" onClick={() => props.added(props.category, props.value)}>
      <td>{props.category}</td>
      <td>{props.label}</td>
      <td>{props.definition}</td>
    </tr>
  )
}

function FilterBox(props) {
  const [showBox, setShowBox] = useState(false);
  const [textFilter, setTextFilter] = useState("");

  const escFunction = useCallback((event) => {
    if(event.keyCode === 27) clear_all();
//    if(event.keyCode === 13) try_enter();
  }, []);

  useEffect(() => {
    document.addEventListener("keydown", escFunction, false);

    return () => {
      document.removeEventListener("keydown", escFunction, false);
    };
  }, [escFunction]);

  function added(category, uri){
    setShowBox(false);
    setTextFilter("");
    props.added(category, uri);
  }

  function clear_all(){
      setTextFilter("");
      setShowBox(false);
  }

  const category_filters = props.data.map(row =>
    <CategoryTableRow data={row} key={row.name} added={added}/>
  );

  var filtersArr = [];
  for(var category of props.data){
    if('choices' in category){
      for(var choice of category.choices){
        if(choice.label.toLowerCase().indexOf(textFilter.toLowerCase()) >= 0){
          filtersArr.push({'category': category.name, 'label': choice.label, 'value': choice.value, 'definition': choice.definition});
        }
      }
    }
    if(category.name.toLowerCase().indexOf(textFilter.toLowerCase()) >= 0){
      filtersArr.push({'category': category.name, 'label': category.name, 'value': '', 'definition': category.definition});
    }
  }
  const filters = filtersArr.map((row, i) =>
    <TermTableRow category={row.category} label={row.label} definition={row.definition} uri={row.value} key={i} added={added}/>
  );

  /*function try_enter(){
    if(filtersArr.length === 1){
      added(filtersArr[0].category, filtersArr[0].value);
    }
  }*/

  return (
    <div className="filter_div">
      <span className="filter_type">{props.must} Criteria</span>
      <div className="filter_container">
        <div className="filter_spreader">
          <div className="filter_search_box">
            <div className="filter_form">
              <input className="filter_search_input"
                     type="text"
                     value={textFilter}
                     onChange={(e) => {
                       setTextFilter(e.target.value);
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
          <div className="filter_results_container" style={{display: (showBox ? 'flex' : 'none')}}>
            <button style={{alignSelf: 'flex-end'}} onClick={() => clear_all()}>Close</button>
            <div className="filter_list">
              <table className="filter_table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {category_filters}
                </tbody>
              </table>
            </div>
          </div>
          <div className="filter_results_container" style={{display: (textFilter !== "" ? 'flex' : 'none')}}>
            <button style={{alignSelf: 'flex-end'}} onClick={() => clear_all()}>Close</button>
            <div className="filter_list">
              <table className="filter_table">
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>Term</th>
                    <th>Definition</th>
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
  const [showCollections, setShowCollections] = useState(false);
  const [allData, setAllData] = useState([]);
  const [cohortName, setCohortName] = useState("Unnamed");
  const [fetching, setFetching] = useState(false);

  const config = useFetch("/api/config");
  const metadata = useFetch("/api/collections");

  if(config === null || metadata === null){
    return <span>...loading...</span>
  }

  function reset_all(){
    setMustFilters([]);
    setCannotFilters([]);
    setMustCohort({});
    setCannotCohort({});
    setCurrentCohort([]);
    setShowCohort(false);
    setShowCollections(false);
    setAllData([]);
    setCohortName("Unnamed");
    setFetching(false);
  }

  function displayCohort(){
    setShowCohort(!showCohort);
    if (!showCohort) fetch_all(currentCohort);
  }

  function add_must_filter(category, uri){
    if(mustFilters.indexOf(category) >= 0) return;
    let newFilters = mustFilters.slice();
    newFilters.push(category);
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

  function add_cannot_filter(category, uri){
    if(cannotFilters.indexOf(category) >= 0) return;
    let newFilters = cannotFilters.slice();
    newFilters.push(category);
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
    for(let row of config){
      if(row.name === name){
        return row
      }
    }
  }

  function intersect(a, b) {
      return new Set([...a].filter(i => b.has(i)));
  }

  function update_current_cohort(mustCohort, cannotCohort){
    if(mustCohort.length === 0){
      setCurrentCohort([]);
      setShowCohort(false);
      setAllData([]);
      return;
    }
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
    setShowCohort(false);
    setAllData([]);
    //fetch_all(finalCohort);
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
    setFetching(true);
    setAllData([]);
    let url = '/api/data?';
    let opts = {method: 'POST',
                body: JSON.stringify(
                  {'patient_ids': currentCohort}
                  ),
                headers: {
                  'Content-Type': 'application/json'
                  },
                };
    const response = await fetch(url, opts);
    let data = await response.json();
    setFetching(false);
    setAllData(data);
  }

  let dUrl = '/api/data?';
  let dParams = new URLSearchParams();
  dParams.set('patient_ids', currentCohort.join(','));
  dParams.set('downloadFile', cohortName);
  const downloadLink = dUrl + dParams;
  let disable_download = downloadLink.length > 7000;

  const mustFilterBoxes = mustFilters.map(row =>
    <RedcapFilter data={get_data(row)} key={row} remove={remove_must_filter} fetch={add_must_cohort}/>
  );

  const cannotFilterBoxes = cannotFilters.map(row =>
    <RedcapFilter data={get_data(row)} key={row} remove={remove_cannot_filter} fetch={add_cannot_cohort}/>
  );

  let params = new URLSearchParams();
  params.set('PatientCriteria', currentCohort.join(','));
  const nbia_link = 'https://nbia.cancerimagingarchive.net/nbia-search/?' + params;
//const nbia_link = 'https://portal.aries.uams.edu/nbia-search/?' + params;

  const allFeatures = metadata.features.map((feature) =>
    <th key={feature}>{feature.substr(18)}</th>
  );

  function x_from_features(all_features, my_features){
    return all_features.map((feature) => {
      let x = my_features.indexOf(feature) >= 0;

      return <td key={feature} className="col_feature">{x ? 'X' : ''}</td>
    }
    );
  }

  const concept_count = config.reduce(function(sum, feature) {
    if(Object.keys(feature).includes('choices')){
      return sum + feature['choices'].length;
    } else {
      return sum + 1;
    }
  }, 0);

  return (
    <div>
      <header className="Beam-header">
        <div className="header_section" style={{flexGrow:0}}>
          <h2 className="collection_size">Repository Overview</h2>
          <div className="collection_info">
            <div className="collection_info_category">
              <h4>Subjects</h4>
              <div className="collection_icon_row">
                <img className="collection_icons" src={PersonLogo} alt="Person Icon"/>
                <span>{metadata.total.toLocaleString()}</span>
              </div>
            </div>
            <div className="collection_info_category">
              <h4>Collections</h4>
              <div className="collection_icon_row">
                <img className="collection_icons" src={FilesLogo} alt="Collection Icon"/>
                <span>{metadata.collections.length}</span>
              </div>
            </div>
            <div className="collection_info_category">
              <h4>Concepts</h4>
              <div className="collection_icon_row">
                <img className="collection_icons" src={DataLogo} alt="Data Icon"/>
                <span>{concept_count}</span>
              </div>
            </div>
          </div>
          <button className="show_collection_button" onClick={() => setShowCollections(!showCollections)}>
            <svg className="filter_button" viewBox="0 0 490 490">
              <path opacity="0.4" fill="none" stroke="#000" strokeWidth="36" d="m280,278a153,153 0 1,0-2,2l170,170m-91-117 110,110-26,26-110-110"/>
            </svg>
            <span>{showCollections ? "Hide" : "Show" } Collections</span>
          </button>
        </div>
        <div className="header_section" style={{flexGrow:0}}>
          <h2 className="">Current Cohort - {currentCohort.length} subjects</h2>
          <div className="row_flex">
            <button className="tallButton" onClick={() => reset_all()}>
              <svg version="1.1" viewBox="0 0 70 70" height="3em" with="3em">
                <g>
                  <g fill="#555753">
                    <path d="m32.5 4.999c-5.405 0-10.444 1.577-14.699 4.282l-5.75-5.75v16.11h16.11l-6.395-6.395c3.18-1.787 6.834-2.82 10.734-2.82 12.171 0 22.073 9.902 22.073 22.074 0 2.899-0.577 5.664-1.599 8.202l4.738 2.762c1.47-3.363 2.288-7.068 2.288-10.964 0-15.164-12.337-27.501-27.5-27.501z"/>
                    <path d="m43.227 51.746c-3.179 1.786-6.826 2.827-10.726 2.827-12.171 0-22.073-9.902-22.073-22.073 0-2.739 0.524-5.35 1.439-7.771l-4.731-2.851c-1.375 3.271-2.136 6.858-2.136 10.622 0 15.164 12.336 27.5 27.5 27.5 5.406 0 10.434-1.584 14.691-4.289l5.758 5.759v-16.112h-16.111l6.389 6.388z"/>
                  </g>
                </g>
              </svg>
              <span>Reset Filters</span>
            </button>
            <button className="tallButton"
                    disabled={currentCohort.length == 0}
                    onClick={() => displayCohort()}>
              <svg className="filter_button" viewBox="0 0 490 490">
                <path opacity="0.4" fill="none" stroke="#000" strokeWidth="36" d="m280,278a153,153 0 1,0-2,2l170,170m-91-117 110,110-26,26-110-110"/>
              </svg>
              <span>{showCohort ? "Hide" : "Preview" } Subjects ({currentCohort.length})</span>
            </button>
            <a style={{textDecoration: 'none'}} href={downloadLink}>
              <button className="tallButton"
                      disabled={currentCohort.length == 0}>
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
                <span>Download CSV ({currentCohort.length})</span>
              </button>
            </a>
            <a href={nbia_link} style={{textDecoration: 'none'}} target='_'>
              <button disabled={currentCohort.length == 0 || disable_download} className="tallButton">
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
                <span>{disable_download ? "Too Many Subjects" : "Browse Files"}</span>
              </button>
            </a>
          </div>
        </div>
      </header>
      {
        (showCollections === true)
        ? <div className="collection_table">
            <table>
              <thead>
                <tr>
                  <th>Collection</th>
                  <th>Description</th>
                  <th>Count</th>
                  {allFeatures}
                </tr>
              </thead>
              <tbody>
                {metadata.collections.map((col) =>
                  <tr key={col.link}>
                    <td><a href={col.link}>{col.name}</a></td>
                    <td>{col.desc}</td>
                    <td>{col.count}</td>
                    {x_from_features(metadata.features, col.features)}
                  </tr>
                 )}
              </tbody>
            </table>
          </div>
        : <></>
      }
      {
        (showCohort === true)
        ? <div className="currentCohort">
            {fetching ?
              <span>fetching...</span> :
              <><h3>Sample Records</h3>
              <DataTable data={allData} /></>}
          </div>
        : <></>
      }
      <div className="filters">
        <div className="filter_item_container">
          <FilterBox must="Inclusion" data={config} added={add_must_filter}/>
          {mustFilterBoxes}
        </div>
        <div className="filter_item_container">
          <FilterBox must="Exclusion" data={config} added={add_cannot_filter}/>
          {cannotFilterBoxes}
        </div>
      </div>
    </div>
  );
}

export default Beam;
