
[GlobalParams]
  volumetric_locking_correction = true
  displacements = 'disp_x disp_y'
[]

[Problem]
  coord_type = RZ
  type = ReferenceResidualProblem
  reference_vector = 'ref'
  extra_tag_vectors = 'ref'
[]

[Mesh]
  file = nano_indenter_rz.e
  # file = indenter_rz_fine.e
  displacements = 'disp_x disp_y'

  # For NodalVariableValue to work with distributed mesh
  allow_renumbering = false
[] # Mesh

[Functions]
  [./disp_y]
    type = PiecewiseLinear
    x = '0.   7.5   10.0'
    y = '0.  -2.0   0.0'
  [../]
[] # Functions

[Variables]
  [./disp_x]
    order = FIRST
    family = LAGRANGE
  [../]

  [./disp_y]
    order = FIRST
    family = LAGRANGE
  [../]

[] # Variables

[AuxVariables]
  [saved_x]
  []
  [saved_y]
  []
[]
[Modules/TensorMechanics/Master]
  [./all]
    add_variables = true
    strain = FINITE
    block = 'indenter material_target'
    use_automatic_differentiation = false
    generate_output = 'stress_xx stress_xy stress_xz stress_yy stress_zz'
    save_in = 'saved_x saved_y'
  [../]
[]

[AuxKernels]
[] # AuxKernels

[BCs]

# Symmetries of the Problem
[./symm_x_indenter]
  type = DirichletBC
  variable = disp_x
  boundary = 'indenter_axis'
  value = 0.0
[../]

[./symm_x_material]
  type = DirichletBC
  variable = disp_x
  boundary = 'target_left'
  value = 0.0
[../]

# Material should not fly away
[./material_base_y]
  type = DirichletBC
  variable = disp_y
  boundary = 'target_bot'
  value = 0.0
[../]

# Drive indenter motion
[./disp_y]
  type = FunctionDirichletBC
  variable = disp_y
  boundary = 'indenter_top'
  function = disp_y
[../]

[] # BCs


[Contact]
  [./dummy_name]
    primary = 'indenter_contact_surfaces'
    secondary = 'target_top'
    model = coulomb
    formulation = penalty
    normalize_penalty = true
    friction_coefficient = 0.5
    penalty = 1e8
    tangential_tolerance = 0.005
  [../]
[]


[Dampers]
  [./contact_slip]
    type = ContactSlipDamper
    primary = 'indenter_contact_surfaces'
    secondary = 'target_top'
  [../]
[]

[Materials]
  [./tensor]
    type = ComputeIsotropicElasticityTensor
    block = 'indenter'
    youngs_modulus = 1.0e7
    poissons_ratio = 0.25
  [../]
  [./stress]
    type = ComputeFiniteStrainElasticStress
    block = 'indenter'
  [../]

  [./tensor_2]
    type = ComputeIsotropicElasticityTensor
    block = 'material_target'
    youngs_modulus = 1e6
    poissons_ratio = 0.0
  [../]

  [./power_law_hardening]
    type = IsotropicPowerLawHardeningStressUpdate
    strength_coefficient = 1e5 #K
    strain_hardening_exponent = 0.5 #n
    block = 'material_target'
  [../]
  [./radial_return_stress]
    type = ComputeMultipleInelasticStress
    inelastic_models = 'power_law_hardening'
    tangent_operator = elastic
    block = 'material_target'
  [../]

[]

[Preconditioning]
  [./SMP]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Transient
  solve_type = 'PJFNK'
  petsc_options = '-snes_ksp_ew'

  petsc_options_iname = '-pc_type -snes_linesearch_type -pc_factor_shift_type -pc_factor_shift_amount'
  petsc_options_value = 'lu       basic                 NONZERO               1e-15'
  line_search = 'none'
  automatic_scaling = true
  nl_abs_tol = 5e-03
  nl_rel_tol = 5e-03
  l_max_its = 40
  start_time = 0.0
  dt = 0.025
  end_time = 10.0
[]

[Postprocessors]
  [./indenter_disp]
    type = NodalExtremeValue
    boundary = 'indenter_tip_node'
    variable = disp_y
  [../]
  [./target_depth]
    type = NodalExtremeValue
    boundary = 'target_depth_node'
    variable = disp_y
  [../]
  [resid_y]
    type = NodalSum
    variable = saved_y
    boundary = 'indenter_top'
  []
  [react_y]
    type = SidesetReaction
    direction = '0 1 0'
    stress_tensor = stress
    boundary = 'target_bot'
  []
[]

[Outputs]
  [./out]
    type = Exodus
    elemental_as_nodal = true
  [../]
  perf_graph = true
  csv = true
[]
