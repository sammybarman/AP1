$(document).ready(function() {
  $.ajax({url: "cart_ops", success: function(result) {
    console.log(result);
    itemsect = document.getElementById('itemsect');
    total_price = 0;
    for (var phone in result.phones) {
      row_div = document.createElement('div');
      row_div.setAttribute('class', 'row');
      col_div = document.createElement('div');
      col_div.setAttribute('class', 'col s12 m6 l5');
      col_div.setAttribute('style', 'margin-left: 20px');
      p = document.createElement('p');
      img = document.createElement('img');
      img.setAttribute('style', 'width:70px;height:120px');
      img.setAttribute('src', result.phones[phone].img_link);
      p.appendChild(img);
      col_div.appendChild(p)
      col_div2 = document.createElement('div');
      col_div2.setAttribute('class', 'col s12 m6 l5 center');
      col_div2.setAttribute('style', 'margin-top: 150px');
      b = document.createElement('b');
      b.innerHTML = result.phones[phone].name;
      price = ' - ' + result.phones[phone].price + ' &nbsp;&nbsp;&nbsp;';
      total_price += result.phones[phone].price;
      p = document.createElement('p');
      b2 = document.createElement('b');
      b2.innerHTML = 'Price';
      button = document.createElement('button');
      button.setAttribute('value', result.phones[phone].phone_data_id);
      button.setAttribute('onclick', 'removeItem(this)');
      i = document.createElement('i');
      i.setAttribute('class', 'material-icons');
      i.innerHTML = 'remove_shopping_cart';
      button.appendChild(i);
      console.log(b2);
      p.innerHTML = b2.outerHTML + price;
      p.appendChild(button);
      col_div2.appendChild(b);
      col_div2.appendChild(p);
      row_div.appendChild(col_div);
      row_div.appendChild(col_div2);
      itemsect.appendChild(row_div)
      itemsect.appendChild(document.createElement('hr'));
    }
    document.getElementById('totalprice').innerHTML = 'Total Price - ' + total_price;
  }});
});

function removeItem(elem) {
  console.log(elem.parentNode.parentNode.parentNode);
  body = {'phone_data_id': elem.value};
  $.ajax({
    url: window.location.protocol+"//"+window.location.hostname+':8000'+'/cart_ops',
    type: 'DELETE',
    data: JSON.stringify(body),
    contentType: 'application/json',
    dataType: 'json',
    success: function (data) {
      console.log('Updated Cart');
      console.log(data);
      $(elem.parentNode.parentNode.parentNode).remove();
    },
    error: function (xhr, ajaxOptions, thrownError) {
      window.location.href = window.location.protocol+"//"+window.location.hostname+':8000'+'/login?next='+encodeURIComponent(link);
    }
  });
}

function checkout() {
  $.ajax({url: "checkout", success: function(result) {
    console.log('checked out');
    location.reload(true);
  }});
}
