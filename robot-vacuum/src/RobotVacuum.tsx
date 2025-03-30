import { useState, useEffect } from "react";
import "./index.css"; 

const API_URL = "http://127.0.0.1:5000/simulate"; 

type Grid = number[][]; // Matrice de la pièce (0 = propre, 1 = sale)
type Position = [number, number]; // Position du robot [x, y]

export default function RobotVacuum (){
  const [grid, setGrid] = useState<Grid>([]);
  const [robotPosition, setRobotPosition] = useState<Position>([0, 0]);
  const [cleanedCount, setCleanedCount] = useState<number>(0);

  // Fonction pour récupérer l'état de la pièce depuis Flask
  const fetchRoomState = async () => {
    try {
      const response = await fetch(API_URL);
      const data: { grid: Grid; robot_position: Position; cleaned_count: number } = await response.json();
      setGrid(data.grid);
      setRobotPosition(data.robot_position);
      setCleanedCount(data.cleaned_count);
    } catch (error) {
      console.error("Erreur lors de la récupération des données :", error);
    }
  };

  useEffect(() => {
    fetchRoomState(); // Charger la pièce au démarrage
  }, []);

  return (
    <div className="container">
      <h1>Robot Aspirateur</h1>
      <p>Cases nettoyées : {cleanedCount}</p>

      {/* Grille */}
      <div className="grid">
        {grid.map((row, y) =>
          row.map((cell, x) => {
            let cellClass = "cell";
            if (x === robotPosition[0] && y === robotPosition[1]) {
              cellClass += " robot";
            } else if (cell === 1) {
              cellClass += " dirty";
            } else {
              cellClass += " clean";
            }
            return <div key={`${x}-${y}`} className={cellClass}></div>;
          })
        )}
      </div>

      {/* Bouton de simulation */}
      <button onClick={fetchRoomState} className="simulate-btn">
        Simuler un mouvement
      </button>
    </div>
  );
};

