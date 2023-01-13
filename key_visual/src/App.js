import { useEffect } from 'react';
import './App.css';
import React,{useState} from "react";
function App() {
  
  var multsize = 3;
  var numdots = 100;
  var depth = 50;
  var inicial = []
  var ppal = 5;
  var colors = {1:"#f5deb9",2:"#a371cf",3:"#778eb8",4:"#324e76"}
  var mensaje = ["Eres la respuesta al llamado de un mundo que siempre necesita sanar","Eres un profesional de la salud, un hereo","Respondiendo al llamado de la naturaleza","Encontrarás todo lo que necesitas para tu camino","Aquí y ahora."]
  var dot = {}
  for(var i = 0; i< numdots;i++){
    dot = {"key":i+ppal,"x":Math.floor(Math.random() * 99),"y":Math.floor(Math.random() * 99),"z":Math.floor(Math.random() * depth),"color":colors[Math.round(1+(Math.random()*2))]}
    if(i<ppal){
      
      dot["secuencia"]=""+i;
      if(i < mensaje.length){
        dot["texto"]=mensaje[i];
      }
        
      if(i < 5){
        dot["z"]=(Math.floor(Math.random()*5))+3;
        dot["x"] = (Math.floor(Math.random() * 40))+30
        dot["y"] = (Math.floor(Math.random() * 40))+30
      }
      
      
    }else{
      dot["secuencia"]="";
      dot["texto"]="";
    }
    inicial.push(dot)
    
  }
  
  const [current,setCurrent] = useState('0')
  const [items,setItems] = useState(inicial)
  const [texto,setTexto] = useState('')
  
  const handleKeyDown = e => {
    if(e.code == "Space"){
      MoveNext();
    }
    if(e.code == "KeyB"){
      MoveBack();
    }
  };
  /*
  const Derecha = () => {
    const salida = items.map((item) => {
      return {...item , x:item.x+(50*(item.z/depth))}
    })
    setItems(salida)
  }
  const Izquierda = () => {
    const salida = items.map((item) => {
      return {...item , x:item.x-(50*(item.z/depth))}
    })
    setItems(salida)
  }
  const Arriba = () => {
    const salida = items.map((item) => {
      return {...item , y:item.y+(50*(item.z/depth))}
    })
    setItems(salida)
  }
  const Abajo = () => {
    const salida = items.map((item) => {
      return {...item , y:item.y-(50*(item.z/depth))}
    })
    setItems(salida)
  }
  const Adelante = () => {
    const salida = items.map((item) => {
      var dx = (item.x -50)/100 ;
      var dy = (item.y -50)/100 ;
      return {...item , z:item.z+1, x:item.x+(5*dx), y:item.y+(5*dy)}
    })
    setItems(salida)
  }
  const Atras = () => {
    const salida = items.map((item) => {
      var dx = (item.x -50)/100 ;
      var dy = (item.y -50)/100 ;
      return {...item , z:item.z-1,x:item.x-(5*dx), y:item.y-(5*dy)}
    })
    setItems(salida)
  }
  */
  const MoveNext = () => {
    if(Number(current) < 4){
      const nwcurr = ""+(Number(current)+1)
      setCurrent(nwcurr)
      var poss = items.filter(x => x.secuencia == nwcurr)[0]
      setTexto(poss.texto)
      var diff = {"x":50-poss.x,"y":50-poss.y,"z":5-poss.z }
      console.log("next........",poss,nwcurr,diff,items)
      const salidaz = items.map((item) => {
        var dx = (item.x -diff.x)/100 ;
        var dy = (item.y -diff.y)/100 ;
        if(item.secuencia == nwcurr){
          item["prevcolor"] = item.color;
          item.color = "white";
        }
        else if(typeof item.prevcolor != "undefined"){
          item.color = item.prevcolor;

        }
        return {...item , z:item.z+diff.z, x:item.x+(2*dx), y:item.y+(2*dy)}
      })
      poss = salidaz.filter(x => x.secuencia == nwcurr)[0]
      diff = {"x":50-poss.x,"y":50-poss.y,"z":5-poss.z };
      const salidas = salidaz.map((item) => {
        var sal = {...item , y:item.y+(diff.y*(item.z/5)),x:item.x+(diff.x*(item.z/5))}//,"color":(item.secuencia == current)?"white":"white"}
        
        return sal;
      })
      setItems(salidas)
      console.log("salida_next.....",nwcurr,salidas)
    }else{
      window.parent.location.href = 'https://nutrabiotics.co/items';

    }
    
  }
  const MoveBack = () => {
    if(Number(current) > -1){
      const nwcurr =""+(Number(current)-1)
      setCurrent(nwcurr)
      var poss = items.filter(x => x.secuencia == nwcurr)[0]
      setTexto(poss.texto)
      var diff = {"x":50-poss.x,"y":50-poss.y,"z":5-poss.z }
      console.log("back........",poss,nwcurr,diff,items)
      const salidaz = items.map((item) => {
        var dx = (item.x -diff.x)/100 ;
        var dy = (item.y -diff.y)/100 ;
        if(item.secuencia == nwcurr){
          item["prevcolor"] = item.color;
          item.color = "white";
        }
        else if(typeof item.prevcolor != "undefined"){
          item.color = item.prevcolor;

        }
        return {...item , z:item.z+diff.z, x:item.x+(2*dx), y:item.y+(2*dy)}
      })
      poss = salidaz.filter(x => x.secuencia == nwcurr)[0]
      diff = {"x":50-poss.x,"y":50-poss.y,"z":5-poss.z };
      const salidas = salidaz.map((item) => {
        var sal = {...item , y:item.y+(diff.y*(item.z/5)),x:item.x+(diff.x*(item.z/5))}
        
        return sal;
      })
      setItems(salidas)
      console.log("salida_back.....",nwcurr,salidas)
    }
    
  }
  return (
    <div className="App-header" tabIndex={0} onKeyDown={handleKeyDown}>
    
    {items.map((item,index)=>{
      var size = (item.z >= 0 && item.z <= depth)?(item.z)*multsize:0;
      var shadow = (item.z >= 0 && item.z <= depth)?(item.z):0;
      var shadow_size = (item.z >= 0 && item.z <= depth)?(item.z):0;
      var opacity = (item.z >= 0 && item.z <= depth)?(1-(item.z/depth)):0;
      return <div 
      key={item.key}
      id={item.x+","+item.y+","+item.z}
      style={{left:item.x+"%" ,
      top:item.y+"%",
      backgroundColor:item.color,
      width:(size)+"px",
      height:(size)+"px",
      boxShadow:"0 0 "+shadow+"px "+shadow_size+"px "+item.color,
      opacity:opacity}} 
      className="dot" >
      
      </div>
      
    })}
    <div className='button_div'>
    
    
    
    <button onClick={MoveBack}>Back</button>
    <button onClick={MoveNext}>Next</button>
    
    </div>
    <div className="texto"><h2>{texto}</h2></div>
    </div>
    
    );
  }
  
  export default App;
  