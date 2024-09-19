var server = 'https://ctppdata.transportation.org/api'
var apiKey = '';
var options = {
  headers: { 'x-api-key': apiKey }
};
var url = '';

// List all available datasets
url = server + '/datasets';
fetch(url, options)
  .then((response) => response.json())
  .then((result) => {
    console.log(result);
  });

// List all groups for year 2016 matching keyword "means of transportation"
url = server + '/groups?year=2016&keyword=means of transportation';
fetch(url, options)
  .then((response) => response.json())
  .then((result) => {
    console.log(result);
  });

// List all variables for group A102106: Means of transportation (18)
url = server + '/groups/A102106/variables?year=2016&page=4';
fetch(url, options)
  .then((response) => response.json())
  .then((result) => {
    console.log(result);
  });

// Get data with geography filter rutned on (Washington, DC)
url = server + '/data/2016?in=state:11&for=county:001&get=group(A102106)';
fetch(url, options)
  .then((response) => response.json())
  .then((result) => {
    console.log(result);
  });
