const user = {
  name : 'kim',
  cart: [],
  purchases: []
}

function addItemToCart(user, item) {
  const updatedCart = user.cart.concat(item)
  return Object.assign({}, user, {cart: updatedCart});
}

function addTaxToItem(user) {
  const taxPrice = 1.3
  const updatedCartWithPrice = user.cart.map(item => {
    return {
      name: item.name,
      price: item.price * taxPrice
    };
  })
  return Object.assign({}, user, {cart: updatedCartWithPrice});
}

function buyItems(user) {
  return Object.assign({}, user, {purchases: user.cart});
}

function emptyCart(user) {
  return Object.assign({}, user, {cart: []});
}

const purchaseItems = (...fns) => fns.reduce(compose) 

const compose = function(f1, f2) {
  return function(...args) {
    console.log(f1.name, f2.name, f1, f2)
    return f1(f2(...args))
  }
}

purchaseItems(
  emptyCart,
  buyItems,
  addTaxToItem,
  addItemToCart) (user, {name: 'Laptop', price: 200})