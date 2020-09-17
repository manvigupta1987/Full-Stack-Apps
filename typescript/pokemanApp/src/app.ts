const container:HTMLElement | any = document.getElementById('app')
const pokemans : number = 100

interface Pokeman {
  id: number;
  name: string;
  image: string;
  type: string
}


const fetchData = (): void => {
  for(let i=1; i<pokemans; i ++) {
    getPokemen(i)
  }
}

const getPokemen = async (id:number): Promise<void> => {
  const data = await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)

  const pokeman:any = await data.json()
  const pokemanType: string = pokeman.types.map((poke:any) => poke.type.name).join(",")

  const transformedPokeman = {
    id: pokeman.id,
    name: pokeman.name,
    image: `${pokeman.sprites.front_default}`,
    type: pokemanType,
  }

  showPokemon(transformedPokeman)
}

const showPokemon = (pokemon: Pokeman): void => {
  let output: string = `
        <div class="card">
            <span class="card--id">#${pokemon.id}</span>
            <img class="card--image" src=${pokemon.image} alt=${pokemon.name} />
            <h1 class="card--name">${pokemon.name}</h1>
            <span class="card--details">${pokemon.type}</span>
        </div>
    `
  container.innerHTML += output
}
fetchData()