import { useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sparkles, Stars } from '@react-three/drei';
import { Activity, CircleDashed, Gauge, HeartPulse, Leaf, RefreshCw, Rocket, Thermometer, Wind } from 'lucide-react';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

type Trait = {
  id: string;
  name: string;
  category: string;
  minimum: number;
  maximum: number;
  baseline: number;
  unit: string;
  description: string;
  affected_genes: string[];
};

type Gene = {
  id: string;
  name: string;
  description: string;
  sequence: string;
  baseline_expression: number;
  protein_id: string;
  traits: string[];
  pathway: string;
  biological_effects: Record<string, number>;
};

type Protein = {
  id: string;
  name: string;
  gene_id: string;
  function: string;
  amino_acid_sequence: string;
  activity: number;
  structural_properties: Record<string, number>;
};

type BiologyMetric = {
  baseline_value: number;
  new_value: number;
  percent_change: number;
  explanation: string;
  contributing_genes: string[];
};

type SimulationState = {
  position: number[];
  energy: number;
  health: number;
  age: number;
  hunger: number;
  temperature: number;
  activity: number;
  flight_speed: number;
  body_size: number;
  behaviour: string;
};

type Mutation = {
  position: number;
  reference: string;
  edited: string;
};

const defaultTraitValues: Record<string, number> = {
  body_size: 1,
  wing_size: 1,
  flight_speed: 1,
  activity: 1,
  navigation: 1,
  feeding_drive: 1,
  metabolism: 1,
  energy_efficiency: 1,
  lifespan: 1,
  reproduction_rate: 1,
  temperature_tolerance: 1,
  stress_resistance: 1,
};

const traitLabels: Record<string, string> = {
  body_size: 'Body Size',
  wing_size: 'Wing Size',
  flight_speed: 'Flight Speed',
  activity: 'Activity',
  navigation: 'Navigation',
  feeding_drive: 'Feeding Drive',
  metabolism: 'Metabolism',
  energy_efficiency: 'Energy Efficiency',
  lifespan: 'Lifespan',
  reproduction_rate: 'Reproduction',
  temperature_tolerance: 'Temp Tolerance',
  stress_resistance: 'Stress Resistance',
};

const metricChartData = [
  { name: 'Base', flight: 1 },
  { name: 'Edited', flight: 1.2 },
  { name: 'Peak', flight: 1.4 },
];

function MosquitoModel({ flightSpeed, bodySize, temperature }: { flightSpeed: number; bodySize: number; temperature: number }) {
  const ref = useRef<any>(null);

  useFrame((state) => {
    if (!ref.current) return;
    const t = state.clock.getElapsedTime();
    ref.current.position.x = Math.sin(t * (0.8 + flightSpeed * 0.7)) * (1.2 + flightSpeed * 0.7);
    ref.current.position.y = 0.55 + Math.sin(t * 3.5) * 0.2 + (bodySize - 1) * 0.35;
    ref.current.position.z = Math.cos(t * (0.7 + flightSpeed * 0.8)) * (1.5 + flightSpeed * 0.8);
    ref.current.rotation.y = t * (1.6 + flightSpeed * 1.2);
    ref.current.rotation.z = Math.sin(t * 7.5) * 0.45;
  });

  const wingLift = 0.36 + flightSpeed * 0.2;
  const bodyScale = 0.7 + bodySize * 0.55;
  const glowColor = temperature > 30 ? '#7ae7c7' : '#8ec5ff';

  return (
    <group ref={ref} scale={bodyScale}>
      <mesh position={[0, 0.55, 0]} castShadow>
        <sphereGeometry args={[0.55, 32, 32]} />
        <meshStandardMaterial color="#9ae8d7" emissive={glowColor} emissiveIntensity={0.4} metalness={0.2} roughness={0.45} />
      </mesh>
      <mesh position={[0.7, 0.5, 0]} rotation={[0, 0, 0.25]} castShadow>
        <boxGeometry args={[0.9, 0.12, 0.18]} />
        <meshStandardMaterial color="#baf7cb" metalness={0.25} roughness={0.35} />
      </mesh>
      <mesh position={[-0.7, 0.5, 0]} rotation={[0, 0, -0.25]} castShadow>
        <boxGeometry args={[0.9, 0.12, 0.18]} />
        <meshStandardMaterial color="#baf7cb" metalness={0.25} roughness={0.35} />
      </mesh>
      <mesh position={[0.15, 0.2, 0.36]} rotation={[0.6, 0, 0.3]}>
        <boxGeometry args={[0.38, 0.08, 0.18]} />
        <meshStandardMaterial color="#f9d29d" emissive="#f9d29d" emissiveIntensity={0.2} />
      </mesh>
      <mesh position={[0.15, 0.2, -0.36]} rotation={[-0.6, 0, 0.3]}>
        <boxGeometry args={[0.38, 0.08, 0.18]} />
        <meshStandardMaterial color="#f9d29d" emissive="#f9d29d" emissiveIntensity={0.2} />
      </mesh>
      <mesh position={[0, 1.05, 0]} castShadow>
        <sphereGeometry args={[0.18, 18, 18]} />
        <meshStandardMaterial color="#dff8ff" emissive="#7ae7c7" emissiveIntensity={0.5} />
      </mesh>
      <mesh position={[0.9, 0.2, 0]} rotation={[0, 0, 0.6]}>
        <boxGeometry args={[0.3, 0.08, 0.08]} />
        <meshStandardMaterial color="#bbd8ff" />
      </mesh>
      <mesh position={[-0.9, 0.2, 0]} rotation={[0, 0, -0.6]}>
        <boxGeometry args={[0.3, 0.08, 0.08]} />
        <meshStandardMaterial color="#bbd8ff" />
      </mesh>
      <mesh position={[0, 0.55, 0.58]} rotation={[0.1, 0, 0]}>
        <boxGeometry args={[0.25, wingLift, 0.08]} />
        <meshStandardMaterial color="#b3e7ff" transparent opacity={0.6} />
      </mesh>
      <mesh position={[0, 0.55, -0.58]} rotation={[-0.1, 0, 0]}>
        <boxGeometry args={[0.25, wingLift, 0.08]} />
        <meshStandardMaterial color="#b3e7ff" transparent opacity={0.6} />
      </mesh>
    </group>
  );
}

function WorldScene({ flightSpeed, bodySize, temperature }: { flightSpeed: number; bodySize: number; temperature: number }) {
  return (
    <>
      <color attach="background" args={['#071a1d']} />
      <fog attach="fog" args={['#071a1d', 4.8, 12]} />
      <ambientLight intensity={0.9} />
      <directionalLight position={[6, 8, 4]} intensity={1.7} color="#dfefff" />
      <pointLight position={[0, 3, 0]} intensity={3.4} color={temperature > 30 ? '#7ae7c7' : '#88b8ff'} />
      <Stars radius={35} depth={10} count={1800} factor={2.5} saturation={0} fade speed={0.8} />
      <Sparkles count={150} scale={[10, 6, 10]} size={2.2} speed={0.9} color="#a5f3ff" />

      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.1, 0]} receiveShadow>
        <circleGeometry args={[6.5, 80]} />
        <meshStandardMaterial color="#113a3d" roughness={0.95} metalness={0.1} />
      </mesh>

      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.98, 0]} receiveShadow>
        <ringGeometry args={[2.1, 4.2, 64]} />
        <meshStandardMaterial color="#1d5257" emissive="#114d51" emissiveIntensity={0.4} />
      </mesh>

      {[...Array(18)].map((_, idx) => {
        const angle = (idx / 18) * Math.PI * 2;
        const radius = 2.4 + (idx % 3) * 0.5;
        return (
          <mesh key={idx} position={[Math.cos(angle) * radius, -0.8, Math.sin(angle) * radius]} rotation={[0, angle, 0]}>
            <cylinderGeometry args={[0.08, 0.12, 0.9 + (idx % 4) * 0.2, 10]} />
            <meshStandardMaterial color={idx % 2 === 0 ? '#2a4d4e' : '#23484f'} />
          </mesh>
        );
      })}

      <MosquitoModel flightSpeed={flightSpeed} bodySize={bodySize} temperature={temperature} />
    </>
  );
}

function App() {
  const [traits, setTraits] = useState<Trait[]>([]);
  const [genome, setGenome] = useState<Gene[]>([]);
  const [protein, setProtein] = useState<Protein | null>(null);
  const [biology, setBiology] = useState<Record<string, BiologyMetric>>({});
  const [simulation, setSimulation] = useState<SimulationState>({
    position: [0, 0, 0],
    energy: 100,
    health: 100,
    age: 0,
    hunger: 0.2,
    temperature: 25,
    activity: 1,
    flight_speed: 1,
    body_size: 1,
    behaviour: 'IDLE',
  });
  const [explanation, setExplanation] = useState<Record<string, { id?: string; description?: string; summary?: string; state?: string }>>({});
  const [mutation, setMutation] = useState<{ gene_id: string; reference_sequence: string; edited_sequence: string; mutations: Mutation[] } | null>(null);
  const [activeTrait, setActiveTrait] = useState<string>('flight_speed');
  const [traitValues, setTraitValues] = useState<Record<string, number>>(defaultTraitValues);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [traitsRes, genomeRes, proteinRes, biologyRes] = await Promise.all([
          fetch(`${API_URL}/api/traits`),
          fetch(`${API_URL}/api/genome`),
          fetch(`${API_URL}/api/proteins`),
          fetch(`${API_URL}/api/biology`),
        ]);

        if (!traitsRes.ok || !genomeRes.ok || !proteinRes.ok || !biologyRes.ok) {
          throw new Error('Failed to load GenomeSim data');
        }

        const traitsData = await traitsRes.json();
        const genomeData = await genomeRes.json();
        const proteinData = await proteinRes.json();
        const biologyData = await biologyRes.json();

        setTraits(traitsData.traits);
        setGenome(genomeData.genes || genomeData);
        setProtein(proteinData.proteins?.[0] ?? null);
        setBiology(biologyData.parameters || {});
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unable to load data');
      } finally {
        setLoading(false);
      }
    };

    void loadData();
  }, []);

  const mutationCount = mutation?.mutations.length ?? 0;
  const chartData = useMemo(() => {
    const flightValue = traitValues.flight_speed ?? 1;
    return [
      { name: 'Baseline', flight: 1 },
      { name: 'Edited', flight: Number(flightValue.toFixed(2)) },
      { name: 'High', flight: Math.max(1.4, Number(flightValue.toFixed(2)) + 0.15) },
    ];
  }, [traitValues]);

  const onTraitChange = (id: string, value: number) => {
    setTraitValues((prev) => ({ ...prev, [id]: value }));
    setActiveTrait(id);
  };

  const applyChanges = async () => {
    try {
      setError(null);
      const response = await fetch(`${API_URL}/api/genome/edit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trait_id: activeTrait, value: traitValues[activeTrait] ?? 1 }),
      });

      if (!response.ok) {
        throw new Error('Gene mutation request failed');
      }

      const mutationData = await response.json();
      setMutation(mutationData);

      const explainRes = await fetch(`${API_URL}/api/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trait_id: activeTrait, value: traitValues[activeTrait] ?? 1 }),
      });

      const explainData = explainRes.ok ? await explainRes.json() : {};
      setExplanation(explainData);

      const simulateRes = await fetch(`${API_URL}/api/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          flight_speed: traitValues.flight_speed ?? 1,
          energy: 90,
          temperature: 29,
          hunger: 0.6,
        }),
      });

      const simData = simulateRes.ok ? await simulateRes.json() : null;
      if (simData?.state) {
        setSimulation(simData.state);
      }

      const biologyRes = await fetch(`${API_URL}/api/biology`);
      const biologyData = biologyRes.ok ? await biologyRes.json() : { parameters: {} };
      setBiology(biologyData.parameters || {});

      const proteinRes = await fetch(`${API_URL}/api/proteins/PROTEIN_FLIGHT`);
      const proteinData = proteinRes.ok ? await proteinRes.json() : null;
      if (proteinData) {
        setProtein(proteinData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to apply genetic changes');
    }
  };

  const resetGenome = async () => {
    await fetch(`${API_URL}/api/reset`, { method: 'POST' });
    setTraitValues(defaultTraitValues);
    setMutation(null);
    setSimulation({
      position: [0, 0, 0],
      energy: 100,
      health: 100,
      age: 0,
      hunger: 0.2,
      temperature: 25,
      activity: 1,
      flight_speed: 1,
      body_size: 1,
      behaviour: 'IDLE',
    });
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Interactive Genome-to-Phenotype Simulation Laboratory</p>
          <h1>GenomeSim Experiment 001</h1>
        </div>
        <div className="topbar-actions">
          <button className="ghost-button" onClick={resetGenome}>Reset</button>
          <button className="primary-button" onClick={applyChanges}>Apply Genetic Changes</button>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <main className="layout-grid">
        <section className="panel trait-panel">
          <div className="panel-header">
            <h2>Trait Editor</h2>
          </div>
          {traits.length === 0 ? (
            <p className="muted">Loading traits…</p>
          ) : (
            <div className="trait-list">
              {traits.map((trait) => (
                <div key={trait.id} className={`trait-card ${activeTrait === trait.id ? 'selected' : ''}`}>
                  <div className="trait-row">
                    <div>
                      <label>{trait.name}</label>
                      <small>{trait.description}</small>
                    </div>
                    <button className="tiny-button" onClick={() => setActiveTrait(trait.id)}>Why?</button>
                  </div>
                  <input
                    type="range"
                    min={trait.minimum}
                    max={trait.maximum}
                    step={0.01}
                    value={traitValues[trait.id] ?? trait.baseline}
                    onChange={(event) => onTraitChange(trait.id, Number(event.target.value))}
                  />
                  <div className="trait-metrics">
                    <span>Current: {((traitValues[trait.id] ?? trait.baseline) - 1) * 100 >= 0 ? '+' : ''}{(((traitValues[trait.id] ?? trait.baseline) - 1) * 100).toFixed(0)}%</span>
                    <span>Baseline: {trait.baseline.toFixed(2)}</span>
                    <span>Sim: {(traitValues[trait.id] ?? trait.baseline).toFixed(2)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="panel world-panel">
          <div className="panel-header">
            <h2>3D World</h2>
          </div>
          <div className="world-canvas">
            <Canvas camera={{ position: [0, 2, 6], fov: 45 }}>
              <WorldScene
                flightSpeed={traitValues.flight_speed ?? 1}
                bodySize={traitValues.body_size ?? 1}
                temperature={simulation.temperature ?? 25}
              />
              <OrbitControls enablePan enableZoom enableRotate />
            </Canvas>
          </div>
        </section>

        <section className="panel genome-panel">
          <div className="panel-header">
            <h2>Genome Viewer</h2>
          </div>
          <div className="tab-row">
            <span>REFERENCE</span>
            <span>EDITED</span>
            <span>DIFF</span>
          </div>
          <div className="sequence-box">
            <p className="mono">5' {genome[0]?.sequence ?? 'ATGCGT...'} 3'</p>
            <p className="mono muted">Mutation count: {mutationCount}</p>
            {mutation && mutation.mutations.length > 0 && (
              <p className="mono muted">
                Positions: {mutation.mutations.map((m) => m.position).join(', ')}
              </p>
            )}
          </div>
        </section>

        <section className="panel biology-panel">
          <div className="panel-header">
            <h2>Biological Effects</h2>
          </div>
          <div className="bio-metrics">
            {Object.entries(biology).slice(0, 4).map(([key, value]) => (
              <div key={key} className="metric-card">
                <label>{key.replace('_', ' ')}</label>
                <strong>{value.new_value.toFixed(2)}</strong>
                <small>{value.percent_change.toFixed(0)}%</small>
              </div>
            ))}
          </div>
        </section>

        <section className="panel causal-panel">
          <div className="panel-header">
            <h2>Causal Pathway</h2>
          </div>
          <div className="pathway-graph">
            {['TRAIT', 'GENE', 'DNA', 'PROTEIN', 'PATHWAY', 'PHENOTYPE', 'BEHAVIOUR'].map((step, index) => (
              <div key={step} className="pathway-node">
                <span>{step}</span>
                {index !== 6 && <span className="arrow">↓</span>}
              </div>
            ))}
          </div>
        </section>

        <section className="panel parameters-panel">
          <div className="panel-header">
            <h2>Parameters</h2>
          </div>
          <div className="parameter-list">
            {Object.entries(biology).map(([key, value]) => (
              <div key={key} className="parameter-row">
                <span>{key}</span>
                <strong>{value.new_value.toFixed(2)}</strong>
              </div>
            ))}
          </div>
        </section>

        <section className="panel chart-panel">
          <div className="panel-header">
            <h2>Simulation Output</h2>
          </div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorFlight" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#7ae7c7" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#7ae7c7" stopOpacity={0.1} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#24424f" strokeDasharray="3 3" />
                <XAxis dataKey="name" stroke="#a4bbbc" />
                <YAxis stroke="#a4bbbc" domain={[0.8, 1.8]} />
                <Tooltip />
                <Area type="monotone" dataKey="flight" stroke="#7ae7c7" fillOpacity={1} fill="url(#colorFlight)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel sim-panel">
          <div className="panel-header">
            <h2>Simulation Controls</h2>
          </div>
          <div className="control-row">
            <button className="primary-button small">Run</button>
            <button className="ghost-button small">Pause</button>
            <button className="ghost-button small">Step</button>
            <button className="ghost-button small">Reset Genome</button>
          </div>
          <div className="status-grid">
            <div><span>Time</span><strong>{simulation.age.toFixed(1)}s</strong></div>
            <div><span>Energy</span><strong>{simulation.energy.toFixed(0)}</strong></div>
            <div><span>Health</span><strong>{simulation.health.toFixed(0)}</strong></div>
            <div><span>Temp</span><strong>{simulation.temperature.toFixed(0)}°C</strong></div>
            <div><span>Behaviour</span><strong>{simulation.behaviour}</strong></div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
