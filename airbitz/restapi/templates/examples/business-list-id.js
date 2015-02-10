var endpoint = '{{ ABSOLUTE_ROOT_URL }}api/v1/business/list/334221';

$.ajax({
  beforeSend: function (xhr) {
    xhr.setRequestHeader (
      'Authorization',
      'Token YOUR_API_TOKEN'
    )
  },
  url: endpoint,
  type: 'GET',
  contentType:'application/json',
  dataType:'json'
});