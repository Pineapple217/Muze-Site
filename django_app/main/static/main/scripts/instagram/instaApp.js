let json;

export async function main() {
  json = await getData();
  console.log(json);
}

async function getData() {
  const data = await fetch(
    "https://www.instagram.com/jeugdhuis_de_muze/?__a=1"
  );
  const json = await data.json;
  return json;
}
