# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def model_input():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import os
    
    
    try:
        del mdb.models['fem']
        del mdb.models['cfd']
    except:
        pass
    
    work_directory = os.getcwd()
    
    ## Define parameters ##
    
    nam = 'cfd'
    nam_fem='fem'
    
    ## Length dimension on microns
    ## MPa, Tonnes, sec, 
    
    dep = 0.04   ##Depth
    rce = 0.005  ##Cell radious
    rver = 0.003 ##Vertix radious
    w_cons=0.0025 ##Constriction width
    w_ex  = 0.015 ##Exterior width
    
    visco = 1e-09 ##Viscocity
    densit= 1e-09 ##Density
    
    dga  = rce*0.165  ##GAP

    msh_size = 0.00025
    mesh_refin = 0.0004 
    
    msh_size_fem = 0.00018
    mesh_refin_fem = 0.0001 
    #msh_size=0.0008 ##mesh size -> FEM size will be msh_size/3
    #mesh_refin=0.00025
    
    ## FOR CFD
    init_increment=4e-08 ##Initial or fixed increment
    time_period   =4e-05 ##Simulation time period
    time_output   =1e-06 ##Time output variables 
    
    ## FOR FEM
    init_increment_FEM=1e-15 ##Initial or fixed increment
    time_period_FEM   =0.001 ##Simulation time period
    time_output_FEM   =0.001 ##Time output variables 
        
    # Boundary conditions

    pr_input = 0.00152135 ##MPa
    pr_output= 0.00107842 ##MPa

    # Cell properties
    
    E=800e-6 ## linear elastic modulus in MPa
    nu=0.4995 ## perfect incompresible
    
    #hyperelastic
    mu = E/(2*(1+nu))
    K = E/(3*(1-2*nu))
    
    C10 = mu/2
    D1 = 2/K
    
    #viscoelastic
    g_i=0.7
    k_i=0
    tau_i=(1-g_i)*E
    
    density = 1.107e-9   
    
    rcell = str(rce)
    rvert = str(rver)
    dgap  = str(dga)
    dwcon = str(w_cons)
    dwex  = str(w_ex)    
    
    
    ## Change work directory
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import os
    os.chdir(work_directory)    
    
    mdb.Model(name=nam, modelType=CFD)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models[nam].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0809816, 
        farPlane=0.10758, width=0.105388, height=0.042139, cameraPosition=(
        0.00247977, -0.000151774, 0.0942809), cameraTarget=(0.00247977, 
        -0.000151774, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.00514107, 
        0.0115277, 0.0942809), cameraTarget=(0.00514107, 0.0115277, 0))
    s.Line(point1=(-0.0415, 0.0215), point2=(-0.00900000003911555, 0.0215))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(-0.00900000003911555, 0.0215), point2=(0.0125, 0.006))
    s.Line(point1=(0.0125, 0.006), point2=(0.0385000000242144, 0.006))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.Line(point1=(0.0385000000242144, 0.006), point2=(0.0385000000242144, 0.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.ArcByCenterEnds(center=(-0.0275, 0.0), point1=(-0.0205, 0.0), point2=(
        -0.0345, 0.0), direction=COUNTERCLOCKWISE)
    s.Line(point1=(-0.0345, 0.0), point2=(-0.0205, 0.0))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s.Spot(point=(0.0, 0.0))
    s.FixedConstraint(entity=v[8])
    s.HorizontalDimension(vertex1=v[5], vertex2=v[8], textPoint=(
        -0.0087642427533865, -0.00270666368305683), value=0.0205)
    s.Line(point1=(-0.0415, 0.0215), point2=(-0.0415, 0.0))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[8], addUndoState=False)
    s.setAsConstruction(objectList=(g[6], g[7]))
    s.AngularDimension(line1=g[4], line2=g[3], textPoint=(0.014194255694747, 
        0.0128654483705759), value=135.0)
    s.ObliqueDimension(vertex1=v[3], vertex2=v[4], textPoint=(0.0325688570737839, 
        0.00229724775999784), value=0.0025)
    s.CoincidentConstraint(entity1=v[8], entity2=v[4])
    s.undo()
    s.ConstructionLine(point1=(-0.009, 0.0), point2=(-0.00399999997857958, 0.0))
    s.HorizontalConstraint(entity=g[9], addUndoState=False)
    s.ConstructionLine(point1=(0.0385000000242144, 0.0035), point2=(
        0.0385000000242144, 0.0))
    s.VerticalConstraint(entity=g[10], addUndoState=False)
    s.CoincidentConstraint(entity1=v[4], entity2=g[10], addUndoState=False)
    s.undo()
    s.CoincidentConstraint(entity1=v[4], entity2=g[9])
    s.undo()
    s.FixedConstraint(entity=g[9])
    s.CoincidentConstraint(entity1=v[4], entity2=g[9])
    s.CoincidentConstraint(entity1=v[9], entity2=g[9])
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-0.0367718189954758, 
        0.0215608049184084), value=0.05)
    s.ObliqueDimension(vertex1=v[0], vertex2=v[9], textPoint=(-0.0367718189954758, 
        0.00738068670034409), value=0.015)
    s.FilletByRadius(radius=0.003, curve1=g[4], nearPoint1=(0.0239180494099855, 
        0.00209658592939377), curve2=g[3], nearPoint2=(0.0203638318926096, 
        0.00370188243687153))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0795109, 
        farPlane=0.109051, width=0.103418, height=0.0410257, cameraPosition=(
        0.00638891, 0.0112907, 0.0942809), cameraTarget=(0.00638891, 0.0112907, 
        0))
    s.ObliqueDimension(vertex1=v[10], vertex2=v[3], textPoint=(0.0398168414831162, 
        0.00516936276108027), value=0.04)
    session.viewports['Viewport: 1'].view.setValues(width=0.0972126, 
        height=0.0385642, cameraPosition=(0.00500784, 0.0111676, 0.0942809), 
        cameraTarget=(0.00500784, 0.0111676, 0))
    s.ConstructionLine(point1=(0.0, 0.006), point2=(0.0, -0.00549999998509884))
    s.VerticalConstraint(entity=g[11], addUndoState=False)
    s.FixedConstraint(entity=g[11])
    s.CoincidentConstraint(entity1=g[11], entity2=v[10])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0764983, 
        farPlane=0.112064, width=0.140914, height=0.0559007, cameraPosition=(
        0.00246909, 0.0163584, 0.0942809), cameraTarget=(0.00246909, 0.0163584, 
        0))
    s.Line(point1=(-0.0637426406871193, 0.0), point2=(0.04, 0.0))
    s.HorizontalConstraint(entity=g[12], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[8], entity2=g[12], addUndoState=False)
    s.RadialDimension(curve=g[6], textPoint=(-0.0371186025440693, 
        0.00819516368210316), radius=0.005)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='r_cell', path='dimensions[7]')
    d[7].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[5]', previousParameter='r_cell')
    d[5].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='w', path='dimensions[2]', previousParameter='r_vert')
    s=mdb.models[nam].sketches['__profile__']
    s.parameters.changeKey('w', 'w_con')
    d[2].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='w_ex', path='dimensions[4]', previousParameter='w_con')
    d[4].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='gap', path='dimensions[0]', expression='0.0205', 
        previousParameter='w_ex')
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['gap'].setValues(expression=dgap)
    d[7].setValues(reference=OFF)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_cell'].setValues(expression=rcell)
    d[5].setValues(reference=OFF)
    d[4].setValues(reference=OFF)
    d[2].setValues(reference=OFF)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    s.parameters['w_con'].setValues(expression=dwcon)
    s.parameters['w_ex'].setValues(expression=dwex)

    s.DistanceDimension(entity1=v[10], entity2=g[8], textPoint=(
        -0.0268880762159824, 0.0281596910208464), value=0.0637426406871193)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0764983, 
        farPlane=0.112064)
    s.delete(objectList=(d[8], ))
    s.delete(objectList=(d[3], ))
    s.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(-0.0122094973921776, 
        0.0122767984867096), curve2=g[2], nearPoint2=(-0.0203939154744148, 
        0.0152936596423388))
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='dimensions_9', path='dimensions[9]', previousParameter='gap')
    d[9].setValues(reference=ON)
    s.HorizontalDimension(vertex1=v[0], vertex2=v[10], textPoint=(
        -0.0262653492391109, 0.0264737959951162), value=0.0637426406871193)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    s.ObliqueDimension(vertex1=v[0], vertex2=v[19], textPoint=(-0.0509075708687305, 
        0.0185767151415348), value=0.0487573593128807)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0939419, 
        farPlane=0.0946199, width=0.00237353, height=0.000941577, 
        cameraPosition=(-0.0143087, 0.0151766, 0.0942809), cameraTarget=(
        -0.0143087, 0.0151766, 0))
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.076957, 
        farPlane=0.111605, width=0.1213, height=0.0481196, cameraPosition=(
        0.00999496, 0.017865, 0.0942809), cameraTarget=(0.00999496, 0.017865, 
        0))
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    s.delete(objectList=(d[9], ))
    s.RadialDimension(curve=g[13], textPoint=(-0.00930273532867432, 
        0.018552428111434), radius=0.003)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='dimensions_12', path='dimensions[12]', 
        previousParameter='gap')
    d[12].setValues(reference=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.065861, 
        farPlane=0.122701, width=0.198993, height=0.0789403, cameraPosition=(
        0.0322679, 0.0147035, 0.0942809), cameraTarget=(0.0322679, 0.0147035, 
        0))
    p = mdb.models[nam].Part(name='fluid', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[nam].parts['fluid']
    p.BaseSolidExtrude(sketch=s, depth=dep)
    s.unsetPrimaryObject()
    p = mdb.models[nam].parts['fluid']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam].sketches['__profile__']
    p = mdb.models[nam].parts['fluid']
    s1 = p.features['Solid extrude-1'].sketch
    mdb.models[nam].ConstrainedSketch(name='__edit__', objectToCopy=s1)
    s2 = mdb.models[nam].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
    s2.unsetPrimaryObject()
    
    del mdb.models[nam].sketches['__edit__']
    p = mdb.models[nam].parts['fluid']
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[8], sketchUpEdge=e[16], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 
        0.02))
    s = mdb.models[nam].ConstrainedSketch(name='__profile__', sheetSize=0.213, 
        gridSpacing=0.005, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[nam].parts['fluid']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.194086, 
        farPlane=0.2452, width=0.123279, height=0.049293, cameraPosition=(
        -0.00891803, 0.00773945, 0.229643), cameraTarget=(-0.00891803, 
        0.00773945, 0.02))
    s.ArcByCenterEnds(center=(-0.05125, 0.0), point1=(-0.0425, 0.0), point2=(
        -0.0575, 0.0), direction=COUNTERCLOCKWISE)
    s.CoincidentConstraint(entity1=v[12], entity2=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[10], entity2=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[11], entity2=g[8], addUndoState=False)
    s.Line(point1=(-0.06, 0.0), point2=(-0.0425, 0.0))
    s.HorizontalConstraint(entity=g[11], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
    s.HorizontalDimension(vertex1=v[10], vertex2=v[5], textPoint=(
        -0.0164673458784819, -0.00231323018670082), value=0.0425)
    s.RadialDimension(curve=g[10], textPoint=(-0.0385704860091209, 
        0.00878741033375263), radius=0.00874999999999999)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='r_cell', path='dimensions[1]', expression=rcell)
    s.Parameter(name='gap', path='dimensions[0]', expression=dgap, 
        previousParameter='r_cell')
    s.ConstructionLine(point1=(-0.06, 0.0), point2=(-0.0444854125380516, 0.0))
    s.HorizontalConstraint(entity=g[12], addUndoState=False)
    s.CoincidentConstraint(entity1=v[11], entity2=g[12], addUndoState=False)
    p = mdb.models[nam].parts['fluid']
    f1, e1 = p.faces, p.edges
    p.CutRevolve(sketchPlane=f1[8], sketchUpEdge=e1[16], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s, angle=90.0, 
        flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models[nam].sketches['__profile__']
    a = mdb.models[nam].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models[nam].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[nam].parts['fluid']
    a.Instance(name='fluid-1', part=p, dependent=ON)
    a = mdb.models[nam].rootAssembly
    a.translate(instanceList=('fluid-1', ), vector=(0.0, 0.0, -1*dep))

    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    mdb.models[nam].Material(name='water_mat')
    mdb.models[nam].materials['water_mat'].Density(table=((visco, ), )) ##Viscosity
    mdb.models[nam].materials['water_mat'].Viscosity(table=((densit, ), )) ##Density
    mdb.models[nam].HomogeneousFluidSection(name='water_sec', 
        material='water_mat')
    p = mdb.models[nam].parts['fluid']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='water_set')
    p = mdb.models[nam].parts['fluid']
    p.SectionAssignment(region=region, sectionName='water_sec', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

    ### Define mesh
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.160112, 
        farPlane=0.301862, width=0.14844, height=0.0516965, 
        viewOffsetX=0.00767693, viewOffsetY=-0.0039496)
    p = mdb.models[nam].parts['fluid']
    p.seedPart(size=msh_size, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models[nam].parts['fluid']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    p = mdb.models[nam].parts['fluid']
    #p.generateMesh()

    ## Define sections
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.165138, 
        farPlane=0.296837, width=0.135279, height=0.0471128, 
        viewOffsetX=0.00520651, viewOffsetY=-0.00114929)
    a = mdb.models[nam].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='esf')
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sym_z')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.213294, 
        farPlane=0.341855, width=0.0956126, height=0.0332985, cameraPosition=(
        0.162437, -0.186882, 0.0900326), cameraUpVector=(0.00403878, 0.819412, 
        0.57319), cameraTarget=(-0.013975, -0.00182233, -0.0129808), 
        viewOffsetX=0.00235383, viewOffsetY=0.00928956)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#100 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sym_y')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.211635, 
        farPlane=0.343728, width=0.0948688, height=0.0330394, cameraPosition=(
        0.185382, -0.0398112, 0.184962), cameraUpVector=(-0.1245, 0.977544, 
        -0.170021), cameraTarget=(-0.0123643, -0.00381126, -0.00366614), 
        viewOffsetX=0.00233552, viewOffsetY=0.00921729)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.206098, 
        farPlane=0.344949, width=0.0923868, height=0.032175, cameraPosition=(
        -0.231892, 0.016892, 0.160985), cameraUpVector=(0.359409, 0.913252, 
        -0.191823), cameraTarget=(-0.0149648, -0.00333795, -0.00787413), 
        viewOffsetX=0.00227442, viewOffsetY=0.00897614)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#200 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='input')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.200222, 
        farPlane=0.350321, width=0.0897527, height=0.0312577, cameraPosition=(
        0.234423, -0.0210244, 0.115133), cameraUpVector=(-0.282534, 0.958223, 
        -0.0445294), cameraTarget=(-0.0136312, -0.00380464, -0.00383194), 
        viewOffsetX=0.00220957, viewOffsetY=0.00872022)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#80 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='output')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.203122, 
        farPlane=0.347896, width=0.0910527, height=0.0317104, cameraPosition=(
        0.219946, 0.0607504, 0.134511), cameraUpVector=(-0.454228, 0.839132, 
        -0.299224), cameraTarget=(-0.0113978, -0.00329647, -0.000982056), 
        viewOffsetX=0.00224157, viewOffsetY=0.00884651)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.200776, 
        farPlane=0.350242, width=0.109247, height=0.038047, 
        viewOffsetX=0.00157901, viewOffsetY=0.00727311)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.195319, 
        farPlane=0.354371, width=0.106278, height=0.0370129, cameraPosition=(
        0.243546, 0.0623442, -0.0911679), cameraUpVector=(-0.628446, 0.752069, 
        -0.198615), cameraTarget=(-0.00824535, -0.00153661, 0.00103258), 
        viewOffsetX=0.00153609, viewOffsetY=0.00707542)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.210105, 
        farPlane=0.340544, width=0.114324, height=0.0398149, cameraPosition=(
        0.168713, 0.0639305, 0.19534), cameraUpVector=(-0.3031, 0.828692, 
        -0.470532), cameraTarget=(-0.012665, -0.00307808, -0.00110952), 
        viewOffsetX=0.00165238, viewOffsetY=0.00761106)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#47c ]', ), )
    a.Surface(side1Faces=side1Faces1, name='walls')
    a = mdb.models[nam].rootAssembly
    f1 = a.instances['fluid-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(faces=faces1, name='esf')


    ## define step
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.211082, 
        farPlane=0.339567, width=0.0953974, height=0.0332235, 
        viewOffsetX=-0.00412363, viewOffsetY=0.0084872)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
        adaptiveMeshConstraints=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    mdb.models[nam].FlowStep(name='Step-1', previous='Initial', timePeriod=time_period, 
        maximumCFL=0.45, incAdjustmentFreq=1, stepGrowthFactor=0.025, 
        incrementation=FIXED_TIME, initialInc=init_increment)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models[nam].fieldOutputRequests['F-Output-1'].setValues(variables=ALL, 
        timeInterval=time_output)

    ## Define boundary conditions
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['input']
    mdb.models[nam].FluidInletOutletBC(name='bc_input', createStepName='Step-1', 
        region=region, pressure=pr_input, momentumType=PRESSURE, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['output']
    mdb.models[nam].FluidInletOutletBC(name='bc_output', createStepName='Step-1', 
        region=region, pressure=pr_output, momentumType=PRESSURE, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['walls']
    mdb.models[nam].FluidWallConditionBC(name='bc_wall', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=0.0, type=NO_SLIP, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['esf']
    mdb.models[nam].FluidWallConditionBC(name='bc_esf', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=0.0, type=NO_SLIP, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['sym_y']
    mdb.models[nam].FluidInletOutletBC(name='bc_sym_y', createStepName='Step-1', 
        region=region, pressure=UNSET, v1=22.0, v2=0.0, v3=22.0, 
        momentumType=VELOCITY, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['sym_z']
    mdb.models[nam].FluidInletOutletBC(name='bc_sym_z', createStepName='Step-1', 
        region=region, pressure=UNSET, v1=22.0, v2=22.0, v3=0.0, 
        momentumType=VELOCITY, distributionType=UNIFORM, fieldName='', 
        localCsys=None)





    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    mdb.Model(name=nam_fem, modelType=STANDARD_EXPLICIT)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.5)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -0.25), point2=(0.0, 0.25))
    s.FixedConstraint(entity=g[2])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.380798, 
        farPlane=0.562011, width=0.634419, height=0.253671, cameraPosition=(
        0.0175353, 0.0338773, 0.471405), cameraTarget=(0.0175353, 0.0338773, 
        0))
    s.ArcByCenterEnds(center=(-0.21, 0.0), point1=(-0.18, 0.0), point2=(-0.2375, 
        0.0), direction=COUNTERCLOCKWISE)
    s.Line(point1=(-0.24, 0.0), point2=(-0.18, 0.0))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(-0.175, 0.1325), point2=(0.02, 0.0325))
    s.Line(point1=(0.02, 0.0325), point2=(0.17, 0.0325))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.AngularDimension(line1=g[6], line2=g[5], textPoint=(0.0315533876419067, 
        0.0672340467572212), value=135.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.391344, 
        farPlane=0.551465, width=0.560573, height=0.224144, cameraPosition=(
        0.0328763, 0.0408185, 0.471405), cameraTarget=(0.0328763, 0.0408185, 
        0))
    s.RadialDimension(curve=g[3], textPoint=(-0.189017027616501, 
        0.0392300821840763), radius=0.025)
    d[1].setValues(value=0.005, )
    s.ConstructionLine(point1=(-0.13, 0.0), point2=(-0.107499999962747, 0.0))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.FixedConstraint(entity=g[7])
    s.DistanceDimension(entity1=g[7], entity2=g[6], textPoint=(-0.037549190223217, 
        0.0219339467585087), value=0.0025)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.416173, 
        farPlane=0.526636, width=0.386722, height=0.15463, cameraPosition=(
        0.0400103, 0.0279557, 0.471405), cameraTarget=(0.0400103, 0.0279557, 
        0))
    s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(0.0632038712501526, 
        -0.0235470551997423), value=0.004)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.437303, 
        farPlane=0.505506, width=0.270231, height=0.108051, cameraPosition=(
        0.0267846, 0.0176059, 0.471405), cameraTarget=(0.0267846, 0.0176059, 
        0))
    d[3].setValues(value=0.04, )
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.457205, 
        farPlane=0.485604, width=0.0994252, height=0.0397549, cameraPosition=(
        0.0317864, -0.000752014, 0.471405), cameraTarget=(0.0317864, 
        -0.000752014, 0))
    s.FilletByRadius(radius=0.003, curve1=g[6], nearPoint1=(0.0246308334171772, 
        0.00259742047637701), curve2=g[5], nearPoint2=(0.0174124650657177, 
        0.00510166864842176))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.451577, 
        farPlane=0.491233, width=0.138834, height=0.0555124, cameraPosition=(
        0.0223925, 0.00777077, 0.471405), cameraTarget=(0.0223925, 0.00777077, 
        0))
    s.ConstructionLine(point1=(0.0, 0.005), point2=(0.0, -0.00958232954144478))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.FixedConstraint(entity=g[2])
    s.CoincidentConstraint(entity1=v[6], entity2=g[2])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.356902, 
        farPlane=0.585907, width=0.907352, height=0.362803, cameraPosition=(
        0.296868, 0.101345, 0.471405), cameraTarget=(0.296868, 0.101345, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.079195, 
        0.0596372, 0.471405), cameraTarget=(0.079195, 0.0596372, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.438187, 
        farPlane=0.504623, width=0.232589, height=0.0930001, cameraPosition=(
        0.0160482, 0.0137212, 0.471405), cameraTarget=(0.0160482, 0.0137212, 
        0))
    s.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(-0.046357199549675, 
        -0.0086134672164917), value=0.23)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.423057, 
        farPlane=0.519753, width=0.338528, height=0.13536, cameraPosition=(
        0.0334515, 0.0386265, 0.471405), cameraTarget=(0.0334515, 0.0386265, 
        0))
    s.ObliqueDimension(vertex1=v[3], vertex2=v[10], textPoint=(-0.0189091414213181, 
        0.0496044605970383), value=0.04)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.419549, 
        farPlane=0.523261, width=0.41092, height=0.164305, cameraPosition=(
        0.0593374, 0.0449361, 0.471405), cameraTarget=(0.0593374, 0.0449361, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.00525795, 
        0.0317399, 0.471405), cameraTarget=(-0.00525795, 0.0317399, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.433348, 
        farPlane=0.509462, width=0.266472, height=0.106548, cameraPosition=(
        0.00340525, 0.0306693, 0.471405), cameraTarget=(0.00340525, 0.0306693, 
        0))
    d[6].setValues(value=0.02, )
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.443475, 
        farPlane=0.499335, width=0.195565, height=0.0781963, cameraPosition=(
        0.0141163, 0.0218511, 0.471405), cameraTarget=(0.0141163, 0.0218511, 
        0))
    s.ObliqueDimension(vertex1=v[9], vertex2=v[5], textPoint=(0.0193017479032278, 
        -0.00444010831415653), value=0.02)
    session.viewports['Viewport: 1'].view.setValues(width=0.208048, 
        height=0.0831876, cameraPosition=(0.0166223, 0.0231677, 0.471405), 
        cameraTarget=(0.0166223, 0.0231677, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0168702, 
        0.0175345, 0.471405), cameraTarget=(-0.0168702, 0.0175345, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.452909, 
        farPlane=0.489901, width=0.12951, height=0.0517842, cameraPosition=(
        0.0156514, 0.0129031, 0.471405), cameraTarget=(0.0156514, 0.0129031, 
        0))
    s.setAsConstruction(objectList=(g[5], g[6], g[8]))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.417797, 
        farPlane=0.525013, width=0.424808, height=0.169858, cameraPosition=(
        0.0941365, 0.0537177, 0.471405), cameraTarget=(0.0941365, 0.0537177, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0608754, 
        0.0301783, 0.471405), cameraTarget=(-0.0608754, 0.0301783, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.455853, 
        farPlane=0.486957, width=0.108894, height=0.0435412, cameraPosition=(
        0.00917284, 0.00974471, 0.471405), cameraTarget=(0.00917284, 
        0.00974471, 0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[4]', expression=rvert)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.452169, 
        farPlane=0.49064, width=0.152428, height=0.0609479, cameraPosition=(
        0.0121135, 0.0151312, 0.471405), cameraTarget=(0.0121135, 0.0151312, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0130024, 
        0.00898842, 0.471405), cameraTarget=(-0.0130024, 0.00898842, 0))
    session.viewports['Viewport: 1'].view.setValues(width=0.162157, 
        height=0.0648382, cameraPosition=(-0.0130208, 0.00967152, 0.471405), 
        cameraTarget=(-0.0130208, 0.00967152, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.0241402, 
        0.0264171, 0.471405), cameraTarget=(0.0241402, 0.0264171, 0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='angle', path='dimensions[0]', expression='135', 
        previousParameter='r_vert')
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0244864, 
        0.00916096, 0.471405), cameraTarget=(-0.0244864, 0.00916096, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.457288, 
        farPlane=0.485522, width=0.0988459, height=0.0395233, cameraPosition=(
        0.0165519, 0.00667466, 0.471405), cameraTarget=(0.0165519, 0.00667466, 
        0))
    s.DistanceDimension(entity1=v[6], entity2=g[7], textPoint=(0.0280340164899826, 
        0.000979564618319273), value=0.0025)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.435878, 
        farPlane=0.506932, width=0.267311, height=0.106884, cameraPosition=(
        0.0680491, 0.0329444, 0.471405), cameraTarget=(0.0680491, 0.0329444, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0367488, 
        0.00921118, 0.471405), cameraTarget=(-0.0367488, 0.00921118, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.428096, 
        farPlane=0.514714, width=0.303245, height=0.121252, cameraPosition=(
        -0.0242148, 0.0137381, 0.471405), cameraTarget=(-0.0242148, 0.0137381, 
        0))
    s.undo()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.461595, 
        farPlane=0.481214, width=0.0686851, height=0.0274636, cameraPosition=(
        -0.100191, 0.00576863, 0.471405), cameraTarget=(-0.100191, 0.00576863, 
        0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[2]', expression=dwcon, 
        previousParameter='angle')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.438079, 
        farPlane=0.504731, width=0.264083, height=0.105593, cameraPosition=(
        -0.0313676, 0.0352532, 0.471405), cameraTarget=(-0.0313676, 0.0352532, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.138902, 
        0.013802, 0.471405), cameraTarget=(-0.138902, 0.013802, 0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_cell', path='dimensions[1]', expression=rcell, 
        previousParameter='w_con')
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='gap', path='dimensions[5]', expression=dgap, 
        previousParameter='r_cell')
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0193643, 
        0.0143009, 0.471405), cameraTarget=(-0.0193643, 0.0143009, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.452309, 
        farPlane=0.490501, width=0.133705, height=0.0534616, cameraPosition=(
        -0.008168, 0.00960801, 0.471405), cameraTarget=(-0.008168, 0.00960801, 
        0))
    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[7])
    p = mdb.models[nam_fem].Part(name='cell', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[nam_fem].parts['cell']
    p.BaseSolidRevolve(sketch=s, angle=90.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['cell']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    p = mdb.models[nam_fem].parts['cell']
    p.features['Solid revolve-1'].setValues(flipRevolveDirection=True)
    p = mdb.models[nam_fem].parts['cell']
    p.regenerate()
    s1 = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=3)
    s1.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0879515, 
        farPlane=0.10061, width=0.044318, height=0.0177204, cameraPosition=(
        -0.00111892, 0.00445612, 0.0942809), cameraTarget=(-0.00111892, 
        0.00445612, 0))
    s1.Line(point1=(-0.0095, 0.011), point2=(0.0005, 0.002))
    s1.Line(point1=(0.0005, 0.002), point2=(0.0124999999767169, 0.002))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.ConstructionLine(point1=(-0.004, 0.0), point2=(0.00249999997206032, 0.0))
    s1.HorizontalConstraint(entity=g[4], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0901764, 
        farPlane=0.0983854, width=0.0287392, height=0.0114913, cameraPosition=(
        -0.000892718, 0.00213613, 0.0942809), cameraTarget=(-0.000892718, 
        0.00213613, 0))
    s1.ConstructionLine(point1=(0.0, -0.001), point2=(0.0, 0.000999999965541065))
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.FixedConstraint(entity=g[5])
    s1.FixedConstraint(entity=g[4])
    s1.DistanceDimension(entity1=g[4], entity2=g[3], textPoint=(
        0.00458660023286939, -0.00060549657791853), value=0.002)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[0]', expression=dwcon)
    s1.AngularDimension(line1=g[3], line2=g[2], textPoint=(0.00246381619945169, 
        0.00464250426739454), value=135.0)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='angle', path='dimensions[1]', expression='135', 
        previousParameter='w_con')
    s1.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(0.00217352109029889, 
        0.00259759370237589), curve2=g[2], nearPoint2=(-0.000112550682388246, 
        0.00317668402567506))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[2]', expression=rvert, 
        previousParameter='angle')
    s1.CoincidentConstraint(entity1=v[3], entity2=g[5])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0877521, 
        farPlane=0.10081, width=0.0457141, height=0.0182787, cameraPosition=(
        0.00391326, 0.00660099, 0.0942809), cameraTarget=(0.00391326, 
        0.00660099, 0))
    s1.ObliqueDimension(vertex1=v[0], vertex2=v[7], textPoint=(
        -0.00843879766762257, 0.00520489644259214), value=0.01)
    s1.ObliqueDimension(vertex1=v[6], vertex2=v[2], textPoint=(0.00899260584264994, 
        0.00129008619114757), value=0.02)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0863882, 
        farPlane=0.102174, width=0.0552637, height=0.0220971, cameraPosition=(
        0.00146632, 0.00714777, 0.0942809), cameraTarget=(0.00146632, 
        0.00714777, 0))
    p = mdb.models[nam_fem].Part(name='Part-2', dimensionality=THREE_D, 
        type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[nam_fem].parts['Part-2']
    p.AnalyticRigidSurfExtrude(sketch=s1, depth=dep-dep/100) 
    s1.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    s = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)
    s.unsetPrimaryObject()
    del mdb.models[nam_fem].sketches['__profile__']
    p1 = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    s1 = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=3)
    s1.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0825296, 
        farPlane=0.106032, cameraPosition=(0.00828914, 0.00755118, 0.0942809), 
        cameraTarget=(0.00828914, 0.00755118, 0))
    s1.Line(point1=(-0.0205, 0.0215), point2=(0.0, 0.006))
    s1.Line(point1=(0.0, 0.006), point2=(0.0260000000707805, 0.006))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(0.00198939442634583, 
        0.00598031468689442), curve2=g[2], nearPoint2=(-0.00160256400704384, 
        0.00719291344285011))
    s1.ConstructionLine(point1=(-0.0095, 0.0), point2=(0.00450000001955777, 0.0))
    s1.HorizontalConstraint(entity=g[5], addUndoState=False)
    s1.ConstructionLine(point1=(0.0, 0.002), point2=(0.0, -0.00300000001303852))
    s1.VerticalConstraint(entity=g[6], addUndoState=False)
    s1.FixedConstraint(entity=g[6])
    s1.FixedConstraint(entity=g[5])
    s1.DistanceDimension(entity1=g[5], entity2=g[3], textPoint=(0.0186229310929775, 
        0.00305905472487211), value=0.0025)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0845205, 
        farPlane=0.104041, width=0.0683415, height=0.0273262, cameraPosition=(
        0.0119144, 0.00717823, 0.0942809), cameraTarget=(0.0119144, 0.00717823, 
        0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[1]', expression=dwcon)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[0]', expression=rvert, 
        previousParameter='w_con')
    s1.ObliqueDimension(vertex1=v[6], vertex2=v[2], textPoint=(0.00846279412508011, 
        0.00448864651843905), value=0.02)
    s1.ObliqueDimension(vertex1=v[0], vertex2=v[7], textPoint=(-0.0115132927894592, 
        0.00577964866533875), value=0.02)
    s1.CoincidentConstraint(entity1=v[3], entity2=g[6])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0845205, 
        farPlane=0.104041, width=0.0773444, height=0.030926, cameraPosition=(
        0.014285, 0.00712491, 0.0942809), cameraTarget=(0.014285, 0.00712491, 
        0))
    s1.setAsConstruction(objectList=(g[2], g[3], g[4]))
    s1.rectangle(point1=(-0.017762511450255, 0.015169187503589), point2=(0.02, 
        0.0))
    s1.CoincidentConstraint(entity1=v[9], entity2=g[5], addUndoState=False)
    p = mdb.models[nam_fem].Part(name='Part-3', dimensionality=TWO_D_PLANAR, 
        type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[nam_fem].parts['Part-3']
    p.AnalyticRigidSurf2DPlanar(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['Part-3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0746496, 
        farPlane=0.0881318, width=0.0531759, height=0.0212623, 
        viewOffsetX=0.00412871, viewOffsetY=0.00299161)
    del mdb.models[nam_fem].parts['Part-3']
    p = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    s = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0851061, 
        farPlane=0.103456, width=0.064241, height=0.0256866, cameraPosition=(
        0.0028233, 0.00286734, 0.0942809), cameraTarget=(0.0028233, 0.00286734, 
        0))
    s.Line(point1=(-0.0085, 0.014), point2=(0.006, 0.005))
    s.Line(point1=(0.006, 0.005), point2=(0.0215000000158325, 0.005))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.undo()
    s.Line(point1=(0.006, 0.005), point2=(0.02, 0.005))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(0.0100828651338816, 
        0.00515284668654203), curve2=g[2], nearPoint2=(0.00379665335640311, 
        0.00632593594491482))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0866605, 
        farPlane=0.101901, width=0.0533576, height=0.0213349, cameraPosition=(
        0.00598346, 0.00335491, 0.0942809), cameraTarget=(0.00598346, 
        0.00335491, 0))
    s.ConstructionLine(point1=(0.0, 0.001), point2=(0.0, -0.00150000000651926))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.ConstructionLine(point1=(-0.0015, 0.0), point2=(0.000999999965541065, 0.0))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.FixedConstraint(entity=g[6])
    s.FixedConstraint(entity=g[5])
    s.DistanceDimension(entity1=g[3], entity2=g[6], textPoint=(0.0105983540415764, 
        0.00243095937184989), value=0.0025)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[1]', expression=dwcon)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[0]', expression=rvert, 
        previousParameter='w_con')
    s.AngularDimension(line1=g[3], line2=g[2], textPoint=(0.00298546627163887, 
        0.00743710529059172), value=135.0)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='angle', path='dimensions[2]', expression='135', 
        previousParameter='r_vert')
    s.CoincidentConstraint(entity1=v[3], entity2=g[5])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0856213, 
        farPlane=0.102941, width=0.0606336, height=0.0242442, cameraPosition=(
        0.00681019, 0.00692188, 0.0942809), cameraTarget=(0.00681019, 
        0.00692188, 0))
    s.setAsConstruction(objectList=(g[2], g[3], g[4]))
    s.Line(point1=(0.02, 0.0), point2=(-0.0132478997111321, 0.0))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.ParallelConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s.CoincidentConstraint(entity1=v[8], entity2=g[6], addUndoState=False)
    s.CoincidentConstraint(entity1=v[9], entity2=g[6], addUndoState=False)
    s.ConstructionLine(point1=(-0.0130941548589165, 0.0143515141717972), point2=(
        -0.0130941548589165, 0.0109999999701977))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[0], entity2=g[8], addUndoState=False)
    s.ConstructionLine(point1=(0.02, 0.0025), point2=(0.02, -0.00200000004749745))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[9], addUndoState=False)
    s.CoincidentConstraint(entity1=v[8], entity2=g[9])
    s.CoincidentConstraint(entity1=v[9], entity2=g[8])
    p = mdb.models[nam_fem].Part(name='Part-3', dimensionality=THREE_D, 
        type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[nam_fem].parts['Part-3']
    p.AnalyticRigidSurfExtrude(sketch=s, depth=w_ex)
    s.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['Part-3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    p1 = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    mdb.models[nam_fem].parts.changeKey(fromName='Part-2', toName='wall')
    p1 = mdb.models[nam_fem].parts['Part-3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    mdb.models[nam_fem].parts.changeKey(fromName='Part-3', toName='wall2')
    a = mdb.models[nam_fem].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models[nam_fem].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[nam_fem].parts['cell']
    a.Instance(name='cell-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.103689, 
        farPlane=0.165104, width=0.0809401, height=0.0323637, 
        viewOffsetX=0.00611489, viewOffsetY=0.000368439)
    a = mdb.models[nam_fem].rootAssembly
    p = mdb.models[nam_fem].parts['wall']
    a.Instance(name='wall-1', part=p, dependent=ON)
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall-1', ), vector=(0.0, 0.0, -0.01))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.142258, 
        farPlane=0.226895, width=0.050983, height=0.0203854, 
        viewOffsetX=0.00611876, viewOffsetY=-0.000862901)
    session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.13417, 
        farPlane=0.240329, cameraPosition=(0.141688, 0.0934977, 0.0271113), 
        cameraUpVector=(-0.765566, 0.638609, -0.0780238), cameraTarget=(
        -0.0132008, -0.000232997, -0.00884131))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.135027, 
        farPlane=0.23892, cameraPosition=(0.13843, 0.102682, 0.0132802), 
        cameraUpVector=(-0.798771, 0.596755, -0.0764704), cameraTarget=(
        -0.0132473, -0.000101908, -0.00903873))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.14671, 
        farPlane=0.2238, cameraPosition=(0.0994085, 0.0735267, 0.118178), 
        cameraUpVector=(-0.354273, 0.720436, -0.596207), cameraTarget=(
        -0.0139126, -0.000598968, -0.00725035))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.108898, 
        0.0728623, 0.109997), cameraTarget=(-0.00442261, -0.00126332, 
        -0.0154317))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall-1', ), vector=(0.0, -0.0025, 0.005))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall-1', ), vector=(0.0, 0.0025, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.132254, 
        farPlane=0.236638, width=0.120616, height=0.048228, cameraPosition=(
        0.112047, 0.0796855, 0.10312), cameraTarget=(-0.00127368, 0.00555993, 
        -0.0223091))
    p1 = mdb.models[nam_fem].parts['wall2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    a = mdb.models[nam_fem].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models[nam_fem].rootAssembly
    p = mdb.models[nam_fem].parts['wall2']
    a.Instance(name='wall2-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.125662, 
        0.0798274, 0.1119), cameraTarget=(0.00515584, 0.00100181, -0.0214817))
    a = mdb.models[nam_fem].rootAssembly
    a.rotate(instanceList=('wall2-1', ), axisPoint=(0.02, 0.0, -0.0075), 
        axisDirection=(-0.033094, 0.0, 0.0), angle=90.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.154613, 
        farPlane=0.259494, cameraPosition=(0.141158, 0.137459, 0.0192856), 
        cameraUpVector=(-0.840932, 0.453197, -0.295714), cameraTarget=(
        0.00547918, 0.00220439, -0.0234143))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.141158, 
        0.137459, 0.0192856), cameraUpVector=(-0.867853, 0.45197, -0.206287), 
        cameraTarget=(0.00547918, 0.00220439, -0.0234143))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161022, 
        farPlane=0.253861, cameraPosition=(0.119379, 0.162503, -0.0272582), 
        cameraUpVector=(-0.956058, 0.278631, -0.0912035), cameraTarget=(
        0.00442764, 0.00341356, -0.0256615))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161561, 
        farPlane=0.253379, cameraPosition=(0.116428, 0.164505, -0.0313857), 
        cameraUpVector=(-0.960522, 0.259341, -0.100696), cameraTarget=(
        0.00426884, 0.00352131, -0.0258836))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.151671, 
        farPlane=0.254753, cameraPosition=(0.139499, 0.119018, 0.0606999), 
        cameraUpVector=(-0.807555, 0.534768, -0.248753), cameraTarget=(
        0.00551321, 0.00106792, -0.0209169))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.160332, 
        farPlane=0.202775, cameraPosition=(-0.0103672, 0.0377894, 0.174944), 
        cameraUpVector=(-0.175886, 0.834391, -0.522356), cameraTarget=(
        0.000400795, -0.00170305, -0.0170197))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.152931, 
        farPlane=0.205493, cameraPosition=(-0.0284136, 0.0476211, 0.170668), 
        cameraUpVector=(-0.125077, 0.802035, -0.584034), cameraTarget=(
        0.00186459, -0.00250053, -0.0166729))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.159388, 
        farPlane=0.206657, cameraPosition=(0.0143457, 0.068053, 0.165469), 
        cameraUpVector=(-0.281519, 0.728009, -0.6251), cameraTarget=(
        -0.00220776, -0.00444644, -0.0161777))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall2-1', ), vector=(-0.003453, 0.0, 0.0075))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161454, 
        farPlane=0.204593, width=0.0708864, height=0.0283438, cameraPosition=(
        0.0214148, 0.0723307, 0.163117), cameraTarget=(0.00486135, 
        -0.000168714, -0.0185293))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.150542, 
        farPlane=0.249546, cameraPosition=(0.137582, 0.0628002, 0.106902), 
        cameraUpVector=(-0.702328, 0.706756, -0.0850394), cameraTarget=(
        -0.0035527, 0.000521592, -0.0144575))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.152349, 
        farPlane=0.26563, cameraPosition=(0.176973, 0.0793498, -0.0104802), 
        cameraUpVector=(-0.678659, 0.728208, -0.0955811), cameraTarget=(
        -0.00281138, 0.000833043, -0.0166665))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.159709, 
        farPlane=0.258268, width=0.0150924, height=0.00603468, cameraPosition=(
        0.178899, 0.0745659, -0.00572279), cameraTarget=(-0.00088582, 
        -0.00395085, -0.0119091))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall2-1', ), vector=(0.0, 0.0, -1*dep))
    session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
    session.viewports['Viewport: 1'].view.setValues(session.views['Bottom'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.173867, 
        farPlane=0.216845, width=0.11085, height=0.044323, cameraPosition=(
        -0.00357352, -0.187856, -0.00909632), cameraTarget=(-0.00357352, 
        0.0075, -0.00909632))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.16473, 
        farPlane=0.22668, cameraPosition=(0.0256829, -0.157344, 0.0915733), 
        cameraUpVector=(-0.443174, 0.408614, 0.797892), cameraTarget=(
        -0.00357352, 0.0075, -0.00909632))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.163425, 
        farPlane=0.21845, cameraPosition=(-0.0198143, -0.119935, 0.138112), 
        cameraUpVector=(0.095048, 0.747093, 0.657889), cameraTarget=(
        -0.00365469, 0.00756674, -0.00901329))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.168898, 
        farPlane=0.212866, cameraPosition=(-0.00539603, -0.0442994, 0.178856), 
        cameraUpVector=(-0.15345, 0.955368, 0.25244), cameraTarget=(
        -0.00398831, 0.00581661, -0.00995607))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161644, 
        farPlane=0.227159, cameraPosition=(0.0466918, 0.0124978, 0.178223), 
        cameraUpVector=(-0.113054, 0.993527, -0.0111199), cameraTarget=(
        -0.00520907, 0.00448548, -0.00994123))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.153241, 
        farPlane=0.241949, cameraPosition=(0.0896439, 0.0548927, 0.153168), 
        cameraUpVector=(-0.259525, 0.954769, -0.145128), cameraTarget=(
        -0.00541972, 0.00427756, -0.00981835))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.151122, 
        farPlane=0.245533, cameraPosition=(0.0992758, 0.0789758, 0.137263), 
        cameraUpVector=(-0.275579, 0.922442, -0.270475), cameraTarget=(
        -0.00531052, 0.00455059, -0.00999866))

    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models[nam_fem].parts['wall2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = mdb.models[nam_fem].parts['cell']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models[nam_fem].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    elemType1 = mesh.ElemType(elemCode=C3D20R)
    elemType2 = mesh.ElemType(elemCode=C3D15)
    elemType3 = mesh.ElemType(elemCode=C3D10)
    p = mdb.models[nam_fem].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models[nam_fem].parts['cell']
    p.seedPart(size=msh_size/3, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models[nam_fem].parts['cell']
    #p.generateMesh()
    p1 = mdb.models[nam_fem].parts['wall']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p = mdb.models[nam_fem].parts['wall']
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v1[3])
    p1 = mdb.models[nam_fem].parts['wall2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models[nam_fem].parts['wall2']
    v2, e1, d2, n1 = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v2[2])
    a = mdb.models[nam_fem].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
        adaptiveMeshConstraints=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)

    mdb.models[nam_fem].ImplicitDynamicsStep(name='Step-1', previous='Initial', 
        timePeriod=time_period_FEM, maxNumInc=1000000, application=QUASI_STATIC, 
        timeIncrementationMethod=FIXED, initialInc=init_increment_FEM, nohaf=OFF, 
        amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF, noStop=OFF, 
        nlgeom=ON)
    mdb.models['fem'].steps['Step-1'].setValues(application=DEFAULT, nohaf=OFF, 
        amplitude=STEP, initialConditions=DEFAULT)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models[nam_fem].fieldOutputRequests['F-Output-1'].setValues(
        timeInterval=time_output_FEM)
    mdb.models[nam_fem].historyOutputRequests['H-Output-1'].setValues(
        timeInterval=time_output_FEM)

    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    a = mdb.models[nam_fem].rootAssembly
    f1 = a.instances['cell-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(faces=faces1, name='esf')
    a = mdb.models[nam_fem].rootAssembly
    f1 = a.instances['cell-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#4 ]', ), )
    a.Set(faces=faces1, name='sz')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.148791, 
        farPlane=0.262383, cameraPosition=(0.1449, -0.059325, 0.0989057), 
        cameraUpVector=(-0.0388684, 0.846507, 0.530957), cameraTarget=(
        -0.00462671, 0.00247773, -0.0105736))
    a = mdb.models[nam_fem].rootAssembly
    f1 = a.instances['cell-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Set(faces=faces1, name='sy')
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='esf')
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#4 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sz')
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sy')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    a = mdb.models[nam_fem].rootAssembly
    r1 = a.instances['wall-1'].referencePoints
    refPoints1=(r1[2], )
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models[nam_fem].EncastreBC(name='encas_1', createStepName='Step-1', 
        region=region, localCsys=None)
    a = mdb.models[nam_fem].rootAssembly
    r1 = a.instances['wall2-1'].referencePoints
    refPoints1=(r1[2], )
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models[nam_fem].EncastreBC(name='encas_2', createStepName='Step-1', 
        region=region, localCsys=None)
    a = mdb.models[nam_fem].rootAssembly
    region = a.sets['sz']
    mdb.models[nam_fem].ZsymmBC(name='sym_z', createStepName='Step-1', region=region, 
        localCsys=None)
    a = mdb.models[nam_fem].rootAssembly
    region = a.sets['sy']
    mdb.models[nam_fem].YsymmBC(name='sym_y', createStepName='Step-1', region=region, 
        localCsys=None)


    ###Define contact properties
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.163227, 
        farPlane=0.204869, width=0.0412933, height=0.016511, cameraPosition=(
        0.0523839, 0.103367, 0.143173), cameraTarget=(-0.00402469, -0.00169042, 
        -0.0115687))
    mdb.models[nam_fem].ContactProperty('IntProp-1')
    mdb.models[nam_fem].interactionProperties['IntProp-1'].TangentialBehavior(
        formulation=FRICTIONLESS)
    mdb.models[nam_fem].interactionProperties['IntProp-1'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['wall-1'].faces
    side2Faces1 = s1.getSequenceFromMask(mask=('[#7 ]', ), )
    region1=regionToolset.Region(side2Faces=side2Faces1)
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region2=regionToolset.Region(side1Faces=side1Faces1)
    mdb.models[nam_fem].SurfaceToSurfaceContactStd(name='Int-1', 
        createStepName='Step-1', master=region1, slave=region2, sliding=FINITE, 
        thickness=ON, interactionProperty='IntProp-1', adjustMethod=NONE, 
        initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['wall2-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region1=regionToolset.Region(side1Faces=side1Faces1)
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region2=regionToolset.Region(side1Faces=side1Faces1)
    mdb.models[nam_fem].SurfaceToSurfaceContactStd(name='Int-2', 
        createStepName='Step-1', master=region1, slave=region2, sliding=FINITE, 
        thickness=ON, interactionProperty='IntProp-1', adjustMethod=NONE, 
        initialClearance=OMIT, datumAxis=None, clearanceRegion=None)


    #Define material properties

    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models[nam_fem].Material(name='hyp_vis')
    mdb.models[nam_fem].materials['hyp_vis'].Hyperelastic(materialType=ISOTROPIC, 
        testData=OFF, type=NEO_HOOKE, volumetricResponse=VOLUMETRIC_DATA, 
        table=((C10, D1), ))
    # mdb.models[nam_fem].materials['hyp_vis'].Viscoelastic(domain=TIME, time=PRONY, 
    #     table=((g_i, k_i, tau_i), ))
    mdb.models[nam_fem].HomogeneousSolidSection(name='cell_sec', material='hyp_vis', 
        thickness=None)
    p = mdb.models[nam_fem].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = regionToolset.Region(cells=cells)
    p = mdb.models[nam_fem].parts['cell']
    p.SectionAssignment(region=region, sectionName='cell_sec', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    mdb.models[nam_fem].materials['hyp_vis'].hyperelastic.setValues(table=((C10, 
        D1), ))
    mdb.models[nam_fem].materials['hyp_vis'].Density(table=((density, ), ))
    
    


    # import section
    # import regionToolset
    # import displayGroupMdbToolset as dgm
    # import part
    # import material
    # import assembly
    # import step
    # import interaction
    # import load
    # import mesh
    # import optimization
    # import job
    # import sketch
    # import visualization
    # import xyPlot
    # import displayGroupOdbToolset as dgo
    # import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0223823, 
        farPlane=0.0381156, width=0.0144329, height=0.00809896, 
        viewOffsetX=-0.00012662, viewOffsetY=-0.000386955)
    p = mdb.models['fem'].parts['cell']
    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
    p = mdb.models['fem'].parts['cell']
    e, d = p.edges, p.datums
    p.DatumPlaneByOffset(plane=d[6], point=p.InterestingPoint(edge=e[0], 
        rule=CENTER))
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[7], cells=pickedCells)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#3 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=STRUCTURED)
    elemType1 = mesh.ElemType(elemCode=C3D8R)
    elemType2 = mesh.ElemType(elemCode=C3D6)
    elemType3 = mesh.ElemType(elemCode=C3D4)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8H, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8H, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models['fem'].parts['cell']
    #p.generateMesh()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0224199, 
        farPlane=0.0380779, width=0.0112874, height=0.0063502, 
        viewOffsetX=-0.000197249, viewOffsetY=-0.000662914)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#2 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['fem'].parts['cell']
    e = p.edges
    p = mdb.models['fem'].parts['cell']
    p.seedPart(size=msh_size_fem, deviationFactor=0.1, minSizeFactor=0.1)
    pickedEdges = e.getSequenceFromMask(mask=('[#100 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=mesh_refin_fem, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['fem'].parts['cell']
    #p.generateMesh()

    #     #Change refinement zone
    # p = mdb.models['cfd'].parts['fluid']
    # f, e = p.faces, p.edges
    # p.DatumPlaneByOffset(plane=f[7], point=p.InterestingPoint(edge=e[14], 
    #     rule=MIDDLE))
    # p = mdb.models['cfd'].parts['fluid']
    # f1, e1, d = p.faces, p.edges, p.datums
    # p.DatumPlaneByOffset(plane=d[6], point=p.InterestingPoint(edge=e1[18], 
    #     rule=MIDDLE))
    # c = p.cells
    # pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    # p.deleteMesh(regions=pickedRegions)
    # p = mdb.models['cfd'].parts['fluid']
    # c = p.cells
    # pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    # d1 = p.datums
    # p.PartitionCellByDatumPlane(datumPlane=d1[6], cells=pickedCells)
    # p = mdb.models['cfd'].parts['fluid']
    # c = p.cells
    # pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    # d = p.datums
    # p.PartitionCellByDatumPlane(datumPlane=d[7], cells=pickedCells)
    # session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    # session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    #     meshTechnique=ON)
    # session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    #     referenceRepresentation=OFF)
    # p = mdb.models['cfd'].parts['fluid']
    # p.generateMesh()
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.227667, 
    #     farPlane=0.323622, width=0.0461408, height=0.0227797, 
    #     viewOffsetX=0.00822343, viewOffsetY=-0.00126461)
    # session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.24308, 
    #     farPlane=0.261163, width=0.0450008, height=0.0222169, 
    #     viewOffsetX=0.00943546, viewOffsetY=-0.00379473)
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.219025, 
    #     farPlane=0.291828, width=0.0405475, height=0.0200183, cameraPosition=(
    #     0.0945114, 0.058801, 0.231483), cameraUpVector=(-0.0655432, 0.978925, 
    #     -0.193417), cameraTarget=(-0.0112043, 0.00764314, 0.00838589), 
    #     viewOffsetX=0.00850173, viewOffsetY=-0.0034192)
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.230369, 
    #     farPlane=0.322422, width=0.0300197, height=0.0139599, 
    #     viewOffsetX=0.00397664, viewOffsetY=-0.00458711)
    # p = mdb.models['cfd'].parts['fluid']
    # c = p.cells
    # pickedRegions = c.getSequenceFromMask(mask=('[#3 ]', ), )
    # p.deleteMesh(regions=pickedRegions)
    # p = mdb.models['cfd'].parts['fluid']
    # e = p.edges
    # pickedEdges = e.getSequenceFromMask(mask=('[#b031 ]', ), )
    # p.seedEdgeBySize(edges=pickedEdges, size=mesh_refin, deviationFactor=0.1, 
    #     minSizeFactor=0.1, constraint=FINER)
    # p = mdb.models['cfd'].parts['fluid']
    # p.generateMesh()
    # p = mdb.models['cfd'].parts['fluid']
    # p.generateMesh(seedConstraintOverride=ON)

def run_cfd_sim():
    
    work_directory = os.getcwd()
    
    try:
        os.mkdir("Results")    
    except:
        pass
    
    os.chdir(work_directory+"\\Results")
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import time
    
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, connectors=OFF)
    mdb.Job(name='cfd_input', model="cfd", description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, scratch='', resultsFormat=ODB, numCpus=3, numDomains=3)
    mdb.jobs['cfd_input'].writeInput(consistencyChecking=OFF)

    fin = open("cfd_input.inp", "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    #data = data.replace("1e-10, 0.5,  , 0.5, 0.5","1e-10, 1.0, 1.0, 1.0")
    data = data.replace('*Fluid Boundary, type=PHYSICAL, velocity inlet, surface=sym_y', '*Fluid Boundary, type=SURFACE')
    data = data.replace('*Fluid Boundary, type=PHYSICAL, velocity inlet, surface=sym_z', '*Fluid Boundary, type=SURFACE')
    data = data.replace('VELX, 22.', '**')
    data = data.replace('VELY, 22.', '**')
    data = data.replace('VELZ, 22.', '**')
    data = data.replace('VELY, 0.', 'sym_y, VELY, 0.')
    data = data.replace('VELZ, 0.', 'sym_z, VELY, 0.')
    data = data.replace('*Output, history, frequency=0', '*SURFACE OUTPUT, surface=esf \nTRACTION, NTRACTION, STRACTION \n*Output, history, frequency=0 \n*Element Output, elset=esf \nDENSITY, PRESSURE, PRESSFORCE, FORCE, AVGPRESS \n*SURFACE OUTPUT, SURFACE=esf \nPRESSFORCE, FORCE, AVGPRESS')

    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open("cfd_input.inp", "wt")
    #overwrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

    time.sleep(5)
    os.system("abaqus job=cfd_input double cpus=3")
    # session.viewports['Viewport: 1'].setValues(displayedObject=a)
    #mdb.jobs['cfd_input'].setValues(numCpus=4, numDomains=4)
    #mdb.jobs['cfd_input'].submit(consistencyChecking=OFF)
    
    try:
        with open("cfd_input.sta", "r") as fp:
            lines = fp.readlines()
            first = lines[0].split(',')[0]
            end = lines[-1].split(',')[0]

        print(first, end)
        
        session.mdbData.summary()
        o1 = session.openOdb(
            name='cfd_input.odb')
        session.viewports['Viewport: 1'].setValues(displayedObject=o1)
        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
            variableLabel='PRESSURE', outputPosition=NODAL, )
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(
            plotState=CONTOURS_ON_DEF)
        session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
            'Viewport: 1', ))
        session.animationController.play(duration=UNLIMITED)
        session.animationController.stop()
        session.animationController.showLastFrame()       
        #mdb.jobs['cfd_input'].submit(consistencyChecking=OFF)
        
    except:
        pass
    
    
    os.chdir(work_directory)
    
    


    
def cfd_create():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.226174, 
        farPlane=0.326617, width=0.0647925, height=0.0308891, 
        viewOffsetX=0.00531799, viewOffsetY=-0.00233631)
    mdb.Model(name='cfd_1', objectToCopy=mdb.models['cfd'])
    p = mdb.models['cfd_1'].parts['fluid']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['cfd_1'].parts['fluid']
    p.features['Cut revolve-1'].suppress()

    session.upgradeOdb(
        'Results/fem.odb', 
        'Results/fem_new.odb')
    session.openOdb('Results/fem_new.odb')
    odb = session.odbs['Results/fem_new.odb']
    # p = mdb.models['cfd_1'].PartFromOdb(name='CELL-1', instance='CELL-1', odb=odb, 
    #     shape=DEFORMED, step=0, frame=-1)
    # p = mdb.models['cfd_1'].parts['CELL-1']
    # session.viewports['Viewport: 1'].setValues(displayedObject=p)
    odb.close()

    # p = mdb.models['Model-1'].PartFromOdb(name='CELL-1', instance='CELL-1', 
    #     odb=odb, shape=DEFORMED, step=0, frame=-1)
    # p = mdb.models['Model-1'].parts['CELL-1']
    # session.viewports['Viewport: 1'].setValues(displayedObject=p)
    # odb.close()
    
    # import sys
    # sys.path.insert(46, 
    #     r'c:/SIMULIA/CAE/2016.HF2/win_b64/code/python2.7/lib/abaqus_plugins/odb2geo')
    
    # import mesh_geo
    # mesh_geo.Run(modelName='Model-1', meshPartName='CELL-1', geoPartName='esf', 
    #     solid=False)


def boundary_fem():
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    
    try:
        # from  abaqus import session
        session.upgradeOdb(
            "Results/cfd_input.odb", 
            "Results/cfd_input_new.odb", )

        f = mdb.models['fem'].MappedField(name='AnalyticalField-1', description='', 
            regionType=MESH, partLevelData=False, localCsys=None)
        f.OdbMeshRegionData(
            odbFileName='Results/cfd_input_new.odb', 
            variableLabel='PRESSURE', stepIndex=0, frameIndex=100, 
            quantityToPlot=FIELD_OUTPUT, averageElementOutput=True, 
            useRegionBoundaries=True, regionBoundaries=ODB_REGIONS, 
            includeFeatureBoundaries=True, averageOnlyDisplayed=False, 
            computeOrder=EXTRAPOLATE_COMPUTE_AVERAGE, averagingThreshold=75.0, 
            transformationType=DEFAULT, numericForm=REAL, complexAngle=0.0, 
            featureAngle=20.0, _coordSystem=LOCAL, dataType=SCALAR, 
            displayDataType=SCALAR, outputPosition=NODAL, 
            displayOutputPosition=NODAL, refinementType=NO_REFINEMENT, 
            refinementLabel='', refinementIndex=-1, sectionPoint=())


        a = mdb.models['fem'].rootAssembly
        region = a.surfaces['esf']
        mdb.models['fem'].Pressure(name='Load-1', createStepName='Step-1', 
            region=region, distributionType=FIELD, field='AnalyticalField-1', 
            magnitude=1.0, amplitude=UNSET)
        
        #import connectorBehavior
        a = mdb.models['fem'].rootAssembly
        a.regenerate()
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
            predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
        mdb.models['fem'].steps['Step-1'].setValues(timeIncrementationMethod=AUTOMATIC, 
            minInc=1e-15, nohaf=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(
            adaptiveMeshConstraints=OFF)
        mdb.Job(name='fem', model='fem', description='', type=ANALYSIS, atTime=None, 
            waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
            numGPUs=0)
        mdb.jobs['fem'].writeInput(consistencyChecking=OFF)
        
    except:
        pass
    


def refin_cfd():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.224388, 
        farPlane=0.326901, width=0.0906961, height=0.0421758, 
        viewOffsetX=0.00343567, viewOffsetY=-0.00144575)
    p = mdb.models['cfd'].parts['fluid']
    f1, v = p.faces, p.vertices
    p.DatumPlaneByOffset(plane=f1[7], point=v[7])
    p = mdb.models['cfd'].parts['fluid']
    f, v1, d = p.faces, p.vertices, p.datums
    p.DatumPlaneByOffset(plane=d[6], point=v1[6])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.226462, 
        farPlane=0.324827, width=0.0593579, height=0.0276028, 
        viewOffsetX=0.00160416, viewOffsetY=-0.00246326)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.243696, 
        farPlane=0.302481, width=0.063875, height=0.0297034, cameraPosition=(
        0.0641577, 0.129096, 0.237492), cameraUpVector=(-0.363146, 0.676706, 
        -0.640464), cameraTarget=(-0.00650272, 0.00420832, 0.00214091), 
        viewOffsetX=0.00172623, viewOffsetY=-0.00265072)
    p = mdb.models['cfd'].parts['fluid']
    f1, v, e, d1 = p.faces, p.vertices, p.edges, p.datums
    p.DatumPlaneByOffset(plane=d1[7], point=p.InterestingPoint(edge=e[0], 
        rule=MIDDLE))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.246549, 
        farPlane=0.299627, width=0.0240122, height=0.0111663, 
        viewOffsetX=0.00166256, viewOffsetY=-0.00402441)
    p = mdb.models['cfd'].parts['fluid']
    f, v1, e1, d = p.faces, p.vertices, p.edges, p.datums
    p.DatumPlaneByOffset(plane=d[8], point=v1[5])
    p = mdb.models['cfd'].parts['fluid']
    f1, v, e, d1 = p.faces, p.vertices, p.edges, p.datums
    p.DatumPlaneByOffset(plane=d1[9], point=v[4])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.243839, 
        farPlane=0.302338, width=0.0613521, height=0.0285302, 
        viewOffsetX=-0.000207517, viewOffsetY=-0.000396174)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.243541, 
        farPlane=0.302635, width=0.0612772, height=0.0284954, 
        viewOffsetX=0.0209422, viewOffsetY=-0.00909742)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.243541, 
        farPlane=0.302635, width=0.0612774, height=0.0284954, cameraPosition=(
        0.0653954, 0.134079, 0.234476), cameraUpVector=(-0.155124, 0.688017, 
        -0.708921), cameraTarget=(-0.00526501, 0.0091917, -0.000875093), 
        viewOffsetX=0.0209422, viewOffsetY=-0.00909743)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.239566, 
        farPlane=0.30661, width=0.126969, height=0.0590436, 
        viewOffsetX=0.0303682, viewOffsetY=-0.00203871)
    p = mdb.models['cfd'].parts['fluid']
    f, v1, e1, d = p.faces, p.vertices, p.edges, p.datums
    p.DatumPlaneByOffset(plane=d[10], point=p.InterestingPoint(edge=e1[2], 
        rule=MIDDLE))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.238082, 
        farPlane=0.308094, width=0.126182, height=0.0586778, 
        viewOffsetX=0.00250777, viewOffsetY=-0.00725555)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.226774, 
        farPlane=0.322477, width=0.120189, height=0.0558909, cameraPosition=(
        0.119014, 0.178398, 0.175651), cameraUpVector=(-0.494497, 0.534038, 
        -0.685766), cameraTarget=(-0.00774245, 0.00774795, 0.000176178), 
        viewOffsetX=0.00238866, viewOffsetY=-0.00691094)
    session.viewports['Viewport: 1'].view.setValues(width=0.102388, 
        height=0.047613, viewOffsetX=0.00452975, viewOffsetY=-0.00751548)
    p = mdb.models['cfd'].parts['fluid']
    f1, v, e, d1 = p.faces, p.vertices, p.edges, p.datums
    p.DatumPlaneByOffset(plane=f1[1], flip=SIDE2, offset=0.0005)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.213833, 
        farPlane=0.356501, width=0.0963312, height=0.0447963, cameraPosition=(
        0.265864, 0.0714649, 0.0146993), cameraUpVector=(-0.529565, 0.840414, 
        -0.115172), cameraTarget=(-0.00280528, 0.0103855, 0.00657508), 
        viewOffsetX=0.00426178, viewOffsetY=-0.00707087)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.216171, 
        farPlane=0.354163, width=0.0881837, height=0.0410075, 
        viewOffsetX=-0.00219646, viewOffsetY=-0.00833658)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.234549, 
        farPlane=0.335024, width=0.0956809, height=0.0444939, cameraPosition=(
        0.14905, 0.155555, 0.18745), cameraUpVector=(-0.509846, 0.632082, 
        -0.583549), cameraTarget=(-0.00607326, 0.0122506, 0.0103051), 
        viewOffsetX=-0.0023832, viewOffsetY=-0.00904533)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.251381, 
        farPlane=0.316288, width=0.102547, height=0.047687, cameraPosition=(
        0.0588312, 0.181264, 0.218005), cameraUpVector=(-0.413707, 0.530562, 
        -0.739832), cameraTarget=(-0.0086583, 0.0126648, 0.0106424), 
        viewOffsetX=-0.00255423, viewOffsetY=-0.00969446)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[11], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.247033, 
        farPlane=0.316312, width=0.100774, height=0.0468623, cameraPosition=(
        0.0664472, 0.219746, 0.172847), cameraUpVector=(-0.270963, 0.363103, 
        -0.891479), cameraTarget=(-0.00663729, 0.0118182, 0.0073037), 
        viewOffsetX=-0.00251005, viewOffsetY=-0.00952679)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[6], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.248981, 
        farPlane=0.314366, width=0.0745415, height=0.0346636, 
        viewOffsetX=-0.00260786, viewOffsetY=-0.00808934)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[7], cells=pickedCells)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[10], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.251007, 
        farPlane=0.312339, width=0.0518425, height=0.024108, 
        viewOffsetX=-0.00037052, viewOffsetY=-0.00875683)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[9], cells=pickedCells)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[8], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.245848, 
        farPlane=0.317498, width=0.123237, height=0.0573083, 
        viewOffsetX=0.00269791, viewOffsetY=0.00189017)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#7f ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[12], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.247508, 
        farPlane=0.315839, width=0.0910548, height=0.0423427, 
        viewOffsetX=0.00632207, viewOffsetY=-0.00137479)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.261578, 
        farPlane=0.302021, width=0.0962313, height=0.0447498, cameraPosition=(
        0.00431001, -0.202038, 0.192835), cameraUpVector=(-0.460735, 0.794753, 
        0.395083), cameraTarget=(-0.00793998, -0.000333771, 0.00536453), 
        viewOffsetX=0.00668148, viewOffsetY=-0.00145295)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.251485, 
        farPlane=0.318458, width=0.0925183, height=0.0430232, cameraPosition=(
        0.0640373, -0.240535, 0.123054), cameraUpVector=(-0.0269441, 0.711858, 
        0.701807), cameraTarget=(-0.00641409, -0.000337417, 0.00763435), 
        viewOffsetX=0.00642368, viewOffsetY=-0.00139689)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.245851, 
        farPlane=0.32471, width=0.0904455, height=0.0420593, cameraPosition=(
        0.0949982, -0.173545, 0.197867), cameraUpVector=(-0.127231, 0.898879, 
        0.419319), cameraTarget=(-0.00527029, 0.00192465, 0.0104194), 
        viewOffsetX=0.00627976, viewOffsetY=-0.00136559)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.24923, 
        farPlane=0.321331, width=0.0493848, height=0.0229651, 
        viewOffsetX=0.00504559, viewOffsetY=-0.00316511)
    p = mdb.models['cfd'].parts['fluid']
    e1, d1 = p.edges, p.datums
    p.DatumPlaneByOffset(plane=d1[12], point=p.InterestingPoint(edge=e1[69], 
        rule=MIDDLE))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.242342, 
        farPlane=0.328219, width=0.134951, height=0.0627554, 
        viewOffsetX=0.0208354, viewOffsetY=0.00624288)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.242292, 
        farPlane=0.328269, width=0.134923, height=0.0627424, 
        viewOffsetX=0.00385236, viewOffsetY=-0.00313277)
    p = mdb.models['cfd'].parts['fluid']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1fc0 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[20], cells=pickedCells)

    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.200218, 
        farPlane=0.304024, width=0.112216, height=0.052183, cameraPosition=(
        0.139793, 0.149973, 0.137549), cameraTarget=(-0.00576893, 0.00441115, 
        -0.00801354))
    p = mdb.models['cfd'].parts['fluid']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    p = mdb.models['cfd'].parts['fluid']
    p.seedPart(size=0.0003, deviationFactor=0.008, minSizeFactor=0.1)
    #0.0006
    p.generateMesh()




def md_i(press_i, press_o):
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import os
    
    
    try:
        del mdb.models['fem']
        del mdb.models['cfd']
    except:
        pass
    
    work_directory = os.getcwd()
    
    ## Define parameters ##
    
    nam = 'cfd'
    nam_fem='fem'
    
    ## Length dimension on microns
    ## MPa, Tonnes, sec, 
    
    dep = 0.01   ##Depth
    rce = 0.005  ##Cell radious
    rver = 0.003 ##Vertix radious
    w_cons=0.0025 ##Constriction width
    w_ex  = 0.015 ##Exterior width
    
    visco = 1e-09 ##Viscocity
    densit= 1e-09 ##Density
    
    dga  = rce*0.165  ##GAP

    msh_size = 0.00025
    mesh_refin = 0.0004 
    
    msh_size_fem = 0.00018
    mesh_refin_fem = 0.0001 
    #msh_size=0.0008 ##mesh size -> FEM size will be msh_size/3
    #mesh_refin=0.00025
    
    ## FOR CFD
    init_increment=4e-08 ##Initial or fixed increment
    time_period   =4e-05 ##Simulation time period
    time_output   =4e-05 ##Time output variables 
    
    ## FOR FEM
    init_increment_FEM=1e-15 ##Initial or fixed increment
    time_period_FEM   =1e-5 ##Simulation time period
    time_output_FEM   =1e-06 ##Time output variables 
        
    # Boundary conditions

    pr_input = press_i ##MPa
    pr_output= press_o ##MPa

    # Cell properties
    
    E=800e-6 ## linear elastic modulus in MPa
    nu=0.4995 ## perfect incompresible
    
    #hyperelastic
    mu = E/(2*(1+nu))
    K = E/(3*(1-2*nu))
    
    C10 = mu/2
    D1 = 2/K
    
    #viscoelastic
    g_i=0.7
    k_i=0
    tau_i=(1-g_i)*E
    
    density = 1.107e-9   
    
    rcell = str(rce)
    rvert = str(rver)
    dgap  = str(dga)
    dwcon = str(w_cons)
    dwex  = str(w_ex)    
    
    
    ## Change work directory
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import os
    os.chdir(work_directory)    
    
    mdb.Model(name=nam, modelType=CFD)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models[nam].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0809816, 
        farPlane=0.10758, width=0.105388, height=0.042139, cameraPosition=(
        0.00247977, -0.000151774, 0.0942809), cameraTarget=(0.00247977, 
        -0.000151774, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.00514107, 
        0.0115277, 0.0942809), cameraTarget=(0.00514107, 0.0115277, 0))
    s.Line(point1=(-0.0415, 0.0215), point2=(-0.00900000003911555, 0.0215))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(-0.00900000003911555, 0.0215), point2=(0.0125, 0.006))
    s.Line(point1=(0.0125, 0.006), point2=(0.0385000000242144, 0.006))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.Line(point1=(0.0385000000242144, 0.006), point2=(0.0385000000242144, 0.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.ArcByCenterEnds(center=(-0.0275, 0.0), point1=(-0.0205, 0.0), point2=(
        -0.0345, 0.0), direction=COUNTERCLOCKWISE)
    s.Line(point1=(-0.0345, 0.0), point2=(-0.0205, 0.0))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s.Spot(point=(0.0, 0.0))
    s.FixedConstraint(entity=v[8])
    s.HorizontalDimension(vertex1=v[5], vertex2=v[8], textPoint=(
        -0.0087642427533865, -0.00270666368305683), value=0.0205)
    s.Line(point1=(-0.0415, 0.0215), point2=(-0.0415, 0.0))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[8], addUndoState=False)
    s.setAsConstruction(objectList=(g[6], g[7]))
    s.AngularDimension(line1=g[4], line2=g[3], textPoint=(0.014194255694747, 
        0.0128654483705759), value=135.0)
    s.ObliqueDimension(vertex1=v[3], vertex2=v[4], textPoint=(0.0325688570737839, 
        0.00229724775999784), value=0.0025)
    s.CoincidentConstraint(entity1=v[8], entity2=v[4])
    s.undo()
    s.ConstructionLine(point1=(-0.009, 0.0), point2=(-0.00399999997857958, 0.0))
    s.HorizontalConstraint(entity=g[9], addUndoState=False)
    s.ConstructionLine(point1=(0.0385000000242144, 0.0035), point2=(
        0.0385000000242144, 0.0))
    s.VerticalConstraint(entity=g[10], addUndoState=False)
    s.CoincidentConstraint(entity1=v[4], entity2=g[10], addUndoState=False)
    s.undo()
    s.CoincidentConstraint(entity1=v[4], entity2=g[9])
    s.undo()
    s.FixedConstraint(entity=g[9])
    s.CoincidentConstraint(entity1=v[4], entity2=g[9])
    s.CoincidentConstraint(entity1=v[9], entity2=g[9])
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-0.0367718189954758, 
        0.0215608049184084), value=0.05)
    s.ObliqueDimension(vertex1=v[0], vertex2=v[9], textPoint=(-0.0367718189954758, 
        0.00738068670034409), value=0.015)
    s.FilletByRadius(radius=0.003, curve1=g[4], nearPoint1=(0.0239180494099855, 
        0.00209658592939377), curve2=g[3], nearPoint2=(0.0203638318926096, 
        0.00370188243687153))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0795109, 
        farPlane=0.109051, width=0.103418, height=0.0410257, cameraPosition=(
        0.00638891, 0.0112907, 0.0942809), cameraTarget=(0.00638891, 0.0112907, 
        0))
    s.ObliqueDimension(vertex1=v[10], vertex2=v[3], textPoint=(0.0398168414831162, 
        0.00516936276108027), value=0.04)
    session.viewports['Viewport: 1'].view.setValues(width=0.0972126, 
        height=0.0385642, cameraPosition=(0.00500784, 0.0111676, 0.0942809), 
        cameraTarget=(0.00500784, 0.0111676, 0))
    s.ConstructionLine(point1=(0.0, 0.006), point2=(0.0, -0.00549999998509884))
    s.VerticalConstraint(entity=g[11], addUndoState=False)
    s.FixedConstraint(entity=g[11])
    s.CoincidentConstraint(entity1=g[11], entity2=v[10])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0764983, 
        farPlane=0.112064, width=0.140914, height=0.0559007, cameraPosition=(
        0.00246909, 0.0163584, 0.0942809), cameraTarget=(0.00246909, 0.0163584, 
        0))
    s.Line(point1=(-0.0637426406871193, 0.0), point2=(0.04, 0.0))
    s.HorizontalConstraint(entity=g[12], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[8], entity2=g[12], addUndoState=False)
    s.RadialDimension(curve=g[6], textPoint=(-0.0371186025440693, 
        0.00819516368210316), radius=0.005)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='r_cell', path='dimensions[7]')
    d[7].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[5]', previousParameter='r_cell')
    d[5].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='w', path='dimensions[2]', previousParameter='r_vert')
    s=mdb.models[nam].sketches['__profile__']
    s.parameters.changeKey('w', 'w_con')
    d[2].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='w_ex', path='dimensions[4]', previousParameter='w_con')
    d[4].setValues(reference=ON)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='gap', path='dimensions[0]', expression='0.0205', 
        previousParameter='w_ex')
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['gap'].setValues(expression=dgap)
    d[7].setValues(reference=OFF)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_cell'].setValues(expression=rcell)
    d[5].setValues(reference=OFF)
    d[4].setValues(reference=OFF)
    d[2].setValues(reference=OFF)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    s.parameters['w_con'].setValues(expression=dwcon)
    s.parameters['w_ex'].setValues(expression=dwex)

    s.DistanceDimension(entity1=v[10], entity2=g[8], textPoint=(
        -0.0268880762159824, 0.0281596910208464), value=0.0637426406871193)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0764983, 
        farPlane=0.112064)
    s.delete(objectList=(d[8], ))
    s.delete(objectList=(d[3], ))
    s.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(-0.0122094973921776, 
        0.0122767984867096), curve2=g[2], nearPoint2=(-0.0203939154744148, 
        0.0152936596423388))
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='dimensions_9', path='dimensions[9]', previousParameter='gap')
    d[9].setValues(reference=ON)
    s.HorizontalDimension(vertex1=v[0], vertex2=v[10], textPoint=(
        -0.0262653492391109, 0.0264737959951162), value=0.0637426406871193)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    s.ObliqueDimension(vertex1=v[0], vertex2=v[19], textPoint=(-0.0509075708687305, 
        0.0185767151415348), value=0.0487573593128807)
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0939419, 
        farPlane=0.0946199, width=0.00237353, height=0.000941577, 
        cameraPosition=(-0.0143087, 0.0151766, 0.0942809), cameraTarget=(
        -0.0143087, 0.0151766, 0))
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.076957, 
        farPlane=0.111605, width=0.1213, height=0.0481196, cameraPosition=(
        0.00999496, 0.017865, 0.0942809), cameraTarget=(0.00999496, 0.017865, 
        0))
    s=mdb.models[nam].sketches['__profile__']
    s.parameters['r_vert'].setValues(expression=rvert)
    s.delete(objectList=(d[9], ))
    s.RadialDimension(curve=g[13], textPoint=(-0.00930273532867432, 
        0.018552428111434), radius=0.003)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='dimensions_12', path='dimensions[12]', 
        previousParameter='gap')
    d[12].setValues(reference=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.065861, 
        farPlane=0.122701, width=0.198993, height=0.0789403, cameraPosition=(
        0.0322679, 0.0147035, 0.0942809), cameraTarget=(0.0322679, 0.0147035, 
        0))
    p = mdb.models[nam].Part(name='fluid', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[nam].parts['fluid']
    p.BaseSolidExtrude(sketch=s, depth=dep)
    s.unsetPrimaryObject()
    p = mdb.models[nam].parts['fluid']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam].sketches['__profile__']
    p = mdb.models[nam].parts['fluid']
    s1 = p.features['Solid extrude-1'].sketch
    mdb.models[nam].ConstrainedSketch(name='__edit__', objectToCopy=s1)
    s2 = mdb.models[nam].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
    s2.unsetPrimaryObject()
    
    del mdb.models[nam].sketches['__edit__']
    p = mdb.models[nam].parts['fluid']
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[8], sketchUpEdge=e[16], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 
        0.02))
    s = mdb.models[nam].ConstrainedSketch(name='__profile__', sheetSize=0.213, 
        gridSpacing=0.005, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[nam].parts['fluid']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.194086, 
        farPlane=0.2452, width=0.123279, height=0.049293, cameraPosition=(
        -0.00891803, 0.00773945, 0.229643), cameraTarget=(-0.00891803, 
        0.00773945, 0.02))
    s.ArcByCenterEnds(center=(-0.05125, 0.0), point1=(-0.0425, 0.0), point2=(
        -0.0575, 0.0), direction=COUNTERCLOCKWISE)
    s.CoincidentConstraint(entity1=v[12], entity2=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[10], entity2=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[11], entity2=g[8], addUndoState=False)
    s.Line(point1=(-0.06, 0.0), point2=(-0.0425, 0.0))
    s.HorizontalConstraint(entity=g[11], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
    s.HorizontalDimension(vertex1=v[10], vertex2=v[5], textPoint=(
        -0.0164673458784819, -0.00231323018670082), value=0.0425)
    s.RadialDimension(curve=g[10], textPoint=(-0.0385704860091209, 
        0.00878741033375263), radius=0.00874999999999999)
    s=mdb.models[nam].sketches['__profile__']
    s.Parameter(name='r_cell', path='dimensions[1]', expression=rcell)
    s.Parameter(name='gap', path='dimensions[0]', expression=dgap, 
        previousParameter='r_cell')
    s.ConstructionLine(point1=(-0.06, 0.0), point2=(-0.0444854125380516, 0.0))
    s.HorizontalConstraint(entity=g[12], addUndoState=False)
    s.CoincidentConstraint(entity1=v[11], entity2=g[12], addUndoState=False)
    p = mdb.models[nam].parts['fluid']
    f1, e1 = p.faces, p.edges
    p.CutRevolve(sketchPlane=f1[8], sketchUpEdge=e1[16], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s, angle=90.0, 
        flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models[nam].sketches['__profile__']
    a = mdb.models[nam].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models[nam].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[nam].parts['fluid']
    a.Instance(name='fluid-1', part=p, dependent=ON)
    a = mdb.models[nam].rootAssembly
    a.translate(instanceList=('fluid-1', ), vector=(0.0, 0.0, -1*dep))

    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    mdb.models[nam].Material(name='water_mat')
    mdb.models[nam].materials['water_mat'].Density(table=((visco, ), )) ##Viscosity
    mdb.models[nam].materials['water_mat'].Viscosity(table=((densit, ), )) ##Density
    mdb.models[nam].HomogeneousFluidSection(name='water_sec', 
        material='water_mat')
    p = mdb.models[nam].parts['fluid']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='water_set')
    p = mdb.models[nam].parts['fluid']
    p.SectionAssignment(region=region, sectionName='water_sec', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

    ### Define mesh
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.160112, 
        farPlane=0.301862, width=0.14844, height=0.0516965, 
        viewOffsetX=0.00767693, viewOffsetY=-0.0039496)
    p = mdb.models[nam].parts['fluid']
    p.seedPart(size=msh_size, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models[nam].parts['fluid']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    p = mdb.models[nam].parts['fluid']
    #p.generateMesh()

    ## Define sections
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.165138, 
        farPlane=0.296837, width=0.135279, height=0.0471128, 
        viewOffsetX=0.00520651, viewOffsetY=-0.00114929)
    a = mdb.models[nam].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='esf')
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sym_z')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.213294, 
        farPlane=0.341855, width=0.0956126, height=0.0332985, cameraPosition=(
        0.162437, -0.186882, 0.0900326), cameraUpVector=(0.00403878, 0.819412, 
        0.57319), cameraTarget=(-0.013975, -0.00182233, -0.0129808), 
        viewOffsetX=0.00235383, viewOffsetY=0.00928956)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#100 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sym_y')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.211635, 
        farPlane=0.343728, width=0.0948688, height=0.0330394, cameraPosition=(
        0.185382, -0.0398112, 0.184962), cameraUpVector=(-0.1245, 0.977544, 
        -0.170021), cameraTarget=(-0.0123643, -0.00381126, -0.00366614), 
        viewOffsetX=0.00233552, viewOffsetY=0.00921729)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.206098, 
        farPlane=0.344949, width=0.0923868, height=0.032175, cameraPosition=(
        -0.231892, 0.016892, 0.160985), cameraUpVector=(0.359409, 0.913252, 
        -0.191823), cameraTarget=(-0.0149648, -0.00333795, -0.00787413), 
        viewOffsetX=0.00227442, viewOffsetY=0.00897614)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#200 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='input')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.200222, 
        farPlane=0.350321, width=0.0897527, height=0.0312577, cameraPosition=(
        0.234423, -0.0210244, 0.115133), cameraUpVector=(-0.282534, 0.958223, 
        -0.0445294), cameraTarget=(-0.0136312, -0.00380464, -0.00383194), 
        viewOffsetX=0.00220957, viewOffsetY=0.00872022)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#80 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='output')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.203122, 
        farPlane=0.347896, width=0.0910527, height=0.0317104, cameraPosition=(
        0.219946, 0.0607504, 0.134511), cameraUpVector=(-0.454228, 0.839132, 
        -0.299224), cameraTarget=(-0.0113978, -0.00329647, -0.000982056), 
        viewOffsetX=0.00224157, viewOffsetY=0.00884651)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.200776, 
        farPlane=0.350242, width=0.109247, height=0.038047, 
        viewOffsetX=0.00157901, viewOffsetY=0.00727311)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.195319, 
        farPlane=0.354371, width=0.106278, height=0.0370129, cameraPosition=(
        0.243546, 0.0623442, -0.0911679), cameraUpVector=(-0.628446, 0.752069, 
        -0.198615), cameraTarget=(-0.00824535, -0.00153661, 0.00103258), 
        viewOffsetX=0.00153609, viewOffsetY=0.00707542)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.210105, 
        farPlane=0.340544, width=0.114324, height=0.0398149, cameraPosition=(
        0.168713, 0.0639305, 0.19534), cameraUpVector=(-0.3031, 0.828692, 
        -0.470532), cameraTarget=(-0.012665, -0.00307808, -0.00110952), 
        viewOffsetX=0.00165238, viewOffsetY=0.00761106)
    a = mdb.models[nam].rootAssembly
    s1 = a.instances['fluid-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#47c ]', ), )
    a.Surface(side1Faces=side1Faces1, name='walls')
    a = mdb.models[nam].rootAssembly
    f1 = a.instances['fluid-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(faces=faces1, name='esf')


    ## define step
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.211082, 
        farPlane=0.339567, width=0.0953974, height=0.0332235, 
        viewOffsetX=-0.00412363, viewOffsetY=0.0084872)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
        adaptiveMeshConstraints=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    mdb.models[nam].FlowStep(name='Step-1', previous='Initial', timePeriod=time_period, 
        maximumCFL=0.45, incAdjustmentFreq=1, stepGrowthFactor=0.025, 
        incrementation=FIXED_TIME, initialInc=init_increment)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models[nam].fieldOutputRequests['F-Output-1'].setValues(variables=ALL, 
        timeInterval=time_output)

    ## Define boundary conditions
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['input']
    mdb.models[nam].FluidInletOutletBC(name='bc_input', createStepName='Step-1', 
        region=region, pressure=pr_input, momentumType=PRESSURE, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['output']
    mdb.models[nam].FluidInletOutletBC(name='bc_output', createStepName='Step-1', 
        region=region, pressure=pr_output, momentumType=PRESSURE, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['walls']
    mdb.models[nam].FluidWallConditionBC(name='bc_wall', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=0.0, type=NO_SLIP, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['esf']
    mdb.models[nam].FluidWallConditionBC(name='bc_esf', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=0.0, type=NO_SLIP, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['sym_y']
    mdb.models[nam].FluidInletOutletBC(name='bc_sym_y', createStepName='Step-1', 
        region=region, pressure=UNSET, v1=22.0, v2=0.0, v3=22.0, 
        momentumType=VELOCITY, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    a = mdb.models[nam].rootAssembly
    region = a.surfaces['sym_z']
    mdb.models[nam].FluidInletOutletBC(name='bc_sym_z', createStepName='Step-1', 
        region=region, pressure=UNSET, v1=22.0, v2=22.0, v3=0.0, 
        momentumType=VELOCITY, distributionType=UNIFORM, fieldName='', 
        localCsys=None)





    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    mdb.Model(name=nam_fem, modelType=STANDARD_EXPLICIT)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.5)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -0.25), point2=(0.0, 0.25))
    s.FixedConstraint(entity=g[2])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.380798, 
        farPlane=0.562011, width=0.634419, height=0.253671, cameraPosition=(
        0.0175353, 0.0338773, 0.471405), cameraTarget=(0.0175353, 0.0338773, 
        0))
    s.ArcByCenterEnds(center=(-0.21, 0.0), point1=(-0.18, 0.0), point2=(-0.2375, 
        0.0), direction=COUNTERCLOCKWISE)
    s.Line(point1=(-0.24, 0.0), point2=(-0.18, 0.0))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(-0.175, 0.1325), point2=(0.02, 0.0325))
    s.Line(point1=(0.02, 0.0325), point2=(0.17, 0.0325))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.AngularDimension(line1=g[6], line2=g[5], textPoint=(0.0315533876419067, 
        0.0672340467572212), value=135.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.391344, 
        farPlane=0.551465, width=0.560573, height=0.224144, cameraPosition=(
        0.0328763, 0.0408185, 0.471405), cameraTarget=(0.0328763, 0.0408185, 
        0))
    s.RadialDimension(curve=g[3], textPoint=(-0.189017027616501, 
        0.0392300821840763), radius=0.025)
    d[1].setValues(value=0.005, )
    s.ConstructionLine(point1=(-0.13, 0.0), point2=(-0.107499999962747, 0.0))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.FixedConstraint(entity=g[7])
    s.DistanceDimension(entity1=g[7], entity2=g[6], textPoint=(-0.037549190223217, 
        0.0219339467585087), value=0.0025)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.416173, 
        farPlane=0.526636, width=0.386722, height=0.15463, cameraPosition=(
        0.0400103, 0.0279557, 0.471405), cameraTarget=(0.0400103, 0.0279557, 
        0))
    s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(0.0632038712501526, 
        -0.0235470551997423), value=0.004)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.437303, 
        farPlane=0.505506, width=0.270231, height=0.108051, cameraPosition=(
        0.0267846, 0.0176059, 0.471405), cameraTarget=(0.0267846, 0.0176059, 
        0))
    d[3].setValues(value=0.04, )
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.457205, 
        farPlane=0.485604, width=0.0994252, height=0.0397549, cameraPosition=(
        0.0317864, -0.000752014, 0.471405), cameraTarget=(0.0317864, 
        -0.000752014, 0))
    s.FilletByRadius(radius=0.003, curve1=g[6], nearPoint1=(0.0246308334171772, 
        0.00259742047637701), curve2=g[5], nearPoint2=(0.0174124650657177, 
        0.00510166864842176))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.451577, 
        farPlane=0.491233, width=0.138834, height=0.0555124, cameraPosition=(
        0.0223925, 0.00777077, 0.471405), cameraTarget=(0.0223925, 0.00777077, 
        0))
    s.ConstructionLine(point1=(0.0, 0.005), point2=(0.0, -0.00958232954144478))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.FixedConstraint(entity=g[2])
    s.CoincidentConstraint(entity1=v[6], entity2=g[2])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.356902, 
        farPlane=0.585907, width=0.907352, height=0.362803, cameraPosition=(
        0.296868, 0.101345, 0.471405), cameraTarget=(0.296868, 0.101345, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.079195, 
        0.0596372, 0.471405), cameraTarget=(0.079195, 0.0596372, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.438187, 
        farPlane=0.504623, width=0.232589, height=0.0930001, cameraPosition=(
        0.0160482, 0.0137212, 0.471405), cameraTarget=(0.0160482, 0.0137212, 
        0))
    s.DistanceDimension(entity1=v[0], entity2=g[2], textPoint=(-0.046357199549675, 
        -0.0086134672164917), value=0.23)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.423057, 
        farPlane=0.519753, width=0.338528, height=0.13536, cameraPosition=(
        0.0334515, 0.0386265, 0.471405), cameraTarget=(0.0334515, 0.0386265, 
        0))
    s.ObliqueDimension(vertex1=v[3], vertex2=v[10], textPoint=(-0.0189091414213181, 
        0.0496044605970383), value=0.04)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.419549, 
        farPlane=0.523261, width=0.41092, height=0.164305, cameraPosition=(
        0.0593374, 0.0449361, 0.471405), cameraTarget=(0.0593374, 0.0449361, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.00525795, 
        0.0317399, 0.471405), cameraTarget=(-0.00525795, 0.0317399, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.433348, 
        farPlane=0.509462, width=0.266472, height=0.106548, cameraPosition=(
        0.00340525, 0.0306693, 0.471405), cameraTarget=(0.00340525, 0.0306693, 
        0))
    d[6].setValues(value=0.02, )
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.443475, 
        farPlane=0.499335, width=0.195565, height=0.0781963, cameraPosition=(
        0.0141163, 0.0218511, 0.471405), cameraTarget=(0.0141163, 0.0218511, 
        0))
    s.ObliqueDimension(vertex1=v[9], vertex2=v[5], textPoint=(0.0193017479032278, 
        -0.00444010831415653), value=0.02)
    session.viewports['Viewport: 1'].view.setValues(width=0.208048, 
        height=0.0831876, cameraPosition=(0.0166223, 0.0231677, 0.471405), 
        cameraTarget=(0.0166223, 0.0231677, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0168702, 
        0.0175345, 0.471405), cameraTarget=(-0.0168702, 0.0175345, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.452909, 
        farPlane=0.489901, width=0.12951, height=0.0517842, cameraPosition=(
        0.0156514, 0.0129031, 0.471405), cameraTarget=(0.0156514, 0.0129031, 
        0))
    s.setAsConstruction(objectList=(g[5], g[6], g[8]))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.417797, 
        farPlane=0.525013, width=0.424808, height=0.169858, cameraPosition=(
        0.0941365, 0.0537177, 0.471405), cameraTarget=(0.0941365, 0.0537177, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0608754, 
        0.0301783, 0.471405), cameraTarget=(-0.0608754, 0.0301783, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.455853, 
        farPlane=0.486957, width=0.108894, height=0.0435412, cameraPosition=(
        0.00917284, 0.00974471, 0.471405), cameraTarget=(0.00917284, 
        0.00974471, 0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[4]', expression=rvert)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.452169, 
        farPlane=0.49064, width=0.152428, height=0.0609479, cameraPosition=(
        0.0121135, 0.0151312, 0.471405), cameraTarget=(0.0121135, 0.0151312, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0130024, 
        0.00898842, 0.471405), cameraTarget=(-0.0130024, 0.00898842, 0))
    session.viewports['Viewport: 1'].view.setValues(width=0.162157, 
        height=0.0648382, cameraPosition=(-0.0130208, 0.00967152, 0.471405), 
        cameraTarget=(-0.0130208, 0.00967152, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.0241402, 
        0.0264171, 0.471405), cameraTarget=(0.0241402, 0.0264171, 0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='angle', path='dimensions[0]', expression='135', 
        previousParameter='r_vert')
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0244864, 
        0.00916096, 0.471405), cameraTarget=(-0.0244864, 0.00916096, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.457288, 
        farPlane=0.485522, width=0.0988459, height=0.0395233, cameraPosition=(
        0.0165519, 0.00667466, 0.471405), cameraTarget=(0.0165519, 0.00667466, 
        0))
    s.DistanceDimension(entity1=v[6], entity2=g[7], textPoint=(0.0280340164899826, 
        0.000979564618319273), value=0.0025)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.435878, 
        farPlane=0.506932, width=0.267311, height=0.106884, cameraPosition=(
        0.0680491, 0.0329444, 0.471405), cameraTarget=(0.0680491, 0.0329444, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0367488, 
        0.00921118, 0.471405), cameraTarget=(-0.0367488, 0.00921118, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.428096, 
        farPlane=0.514714, width=0.303245, height=0.121252, cameraPosition=(
        -0.0242148, 0.0137381, 0.471405), cameraTarget=(-0.0242148, 0.0137381, 
        0))
    s.undo()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.461595, 
        farPlane=0.481214, width=0.0686851, height=0.0274636, cameraPosition=(
        -0.100191, 0.00576863, 0.471405), cameraTarget=(-0.100191, 0.00576863, 
        0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[2]', expression=dwcon, 
        previousParameter='angle')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.438079, 
        farPlane=0.504731, width=0.264083, height=0.105593, cameraPosition=(
        -0.0313676, 0.0352532, 0.471405), cameraTarget=(-0.0313676, 0.0352532, 
        0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.138902, 
        0.013802, 0.471405), cameraTarget=(-0.138902, 0.013802, 0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_cell', path='dimensions[1]', expression=rcell, 
        previousParameter='w_con')
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='gap', path='dimensions[5]', expression=dgap, 
        previousParameter='r_cell')
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0193643, 
        0.0143009, 0.471405), cameraTarget=(-0.0193643, 0.0143009, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.452309, 
        farPlane=0.490501, width=0.133705, height=0.0534616, cameraPosition=(
        -0.008168, 0.00960801, 0.471405), cameraTarget=(-0.008168, 0.00960801, 
        0))
    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[7])
    p = mdb.models[nam_fem].Part(name='cell', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[nam_fem].parts['cell']
    p.BaseSolidRevolve(sketch=s, angle=90.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['cell']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    p = mdb.models[nam_fem].parts['cell']
    p.features['Solid revolve-1'].setValues(flipRevolveDirection=True)
    p = mdb.models[nam_fem].parts['cell']
    p.regenerate()
    s1 = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=3)
    s1.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0879515, 
        farPlane=0.10061, width=0.044318, height=0.0177204, cameraPosition=(
        -0.00111892, 0.00445612, 0.0942809), cameraTarget=(-0.00111892, 
        0.00445612, 0))
    s1.Line(point1=(-0.0095, 0.011), point2=(0.0005, 0.002))
    s1.Line(point1=(0.0005, 0.002), point2=(0.0124999999767169, 0.002))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.ConstructionLine(point1=(-0.004, 0.0), point2=(0.00249999997206032, 0.0))
    s1.HorizontalConstraint(entity=g[4], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0901764, 
        farPlane=0.0983854, width=0.0287392, height=0.0114913, cameraPosition=(
        -0.000892718, 0.00213613, 0.0942809), cameraTarget=(-0.000892718, 
        0.00213613, 0))
    s1.ConstructionLine(point1=(0.0, -0.001), point2=(0.0, 0.000999999965541065))
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.FixedConstraint(entity=g[5])
    s1.FixedConstraint(entity=g[4])
    s1.DistanceDimension(entity1=g[4], entity2=g[3], textPoint=(
        0.00458660023286939, -0.00060549657791853), value=0.002)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[0]', expression=dwcon)
    s1.AngularDimension(line1=g[3], line2=g[2], textPoint=(0.00246381619945169, 
        0.00464250426739454), value=135.0)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='angle', path='dimensions[1]', expression='135', 
        previousParameter='w_con')
    s1.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(0.00217352109029889, 
        0.00259759370237589), curve2=g[2], nearPoint2=(-0.000112550682388246, 
        0.00317668402567506))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[2]', expression=rvert, 
        previousParameter='angle')
    s1.CoincidentConstraint(entity1=v[3], entity2=g[5])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0877521, 
        farPlane=0.10081, width=0.0457141, height=0.0182787, cameraPosition=(
        0.00391326, 0.00660099, 0.0942809), cameraTarget=(0.00391326, 
        0.00660099, 0))
    s1.ObliqueDimension(vertex1=v[0], vertex2=v[7], textPoint=(
        -0.00843879766762257, 0.00520489644259214), value=0.01)
    s1.ObliqueDimension(vertex1=v[6], vertex2=v[2], textPoint=(0.00899260584264994, 
        0.00129008619114757), value=0.02)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0863882, 
        farPlane=0.102174, width=0.0552637, height=0.0220971, cameraPosition=(
        0.00146632, 0.00714777, 0.0942809), cameraTarget=(0.00146632, 
        0.00714777, 0))
    p = mdb.models[nam_fem].Part(name='Part-2', dimensionality=THREE_D, 
        type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[nam_fem].parts['Part-2']
    p.AnalyticRigidSurfExtrude(sketch=s1, depth=dep-dep/100) 
    s1.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    s = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)
    s.unsetPrimaryObject()
    del mdb.models[nam_fem].sketches['__profile__']
    p1 = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    s1 = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=3)
    s1.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0825296, 
        farPlane=0.106032, cameraPosition=(0.00828914, 0.00755118, 0.0942809), 
        cameraTarget=(0.00828914, 0.00755118, 0))
    s1.Line(point1=(-0.0205, 0.0215), point2=(0.0, 0.006))
    s1.Line(point1=(0.0, 0.006), point2=(0.0260000000707805, 0.006))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(0.00198939442634583, 
        0.00598031468689442), curve2=g[2], nearPoint2=(-0.00160256400704384, 
        0.00719291344285011))
    s1.ConstructionLine(point1=(-0.0095, 0.0), point2=(0.00450000001955777, 0.0))
    s1.HorizontalConstraint(entity=g[5], addUndoState=False)
    s1.ConstructionLine(point1=(0.0, 0.002), point2=(0.0, -0.00300000001303852))
    s1.VerticalConstraint(entity=g[6], addUndoState=False)
    s1.FixedConstraint(entity=g[6])
    s1.FixedConstraint(entity=g[5])
    s1.DistanceDimension(entity1=g[5], entity2=g[3], textPoint=(0.0186229310929775, 
        0.00305905472487211), value=0.0025)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0845205, 
        farPlane=0.104041, width=0.0683415, height=0.0273262, cameraPosition=(
        0.0119144, 0.00717823, 0.0942809), cameraTarget=(0.0119144, 0.00717823, 
        0))
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[1]', expression=dwcon)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[0]', expression=rvert, 
        previousParameter='w_con')
    s1.ObliqueDimension(vertex1=v[6], vertex2=v[2], textPoint=(0.00846279412508011, 
        0.00448864651843905), value=0.02)
    s1.ObliqueDimension(vertex1=v[0], vertex2=v[7], textPoint=(-0.0115132927894592, 
        0.00577964866533875), value=0.02)
    s1.CoincidentConstraint(entity1=v[3], entity2=g[6])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0845205, 
        farPlane=0.104041, width=0.0773444, height=0.030926, cameraPosition=(
        0.014285, 0.00712491, 0.0942809), cameraTarget=(0.014285, 0.00712491, 
        0))
    s1.setAsConstruction(objectList=(g[2], g[3], g[4]))
    s1.rectangle(point1=(-0.017762511450255, 0.015169187503589), point2=(0.02, 
        0.0))
    s1.CoincidentConstraint(entity1=v[9], entity2=g[5], addUndoState=False)
    p = mdb.models[nam_fem].Part(name='Part-3', dimensionality=TWO_D_PLANAR, 
        type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[nam_fem].parts['Part-3']
    p.AnalyticRigidSurf2DPlanar(sketch=s1)
    s1.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['Part-3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0746496, 
        farPlane=0.0881318, width=0.0531759, height=0.0212623, 
        viewOffsetX=0.00412871, viewOffsetY=0.00299161)
    del mdb.models[nam_fem].parts['Part-3']
    p = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    s = mdb.models[nam_fem].ConstrainedSketch(name='__profile__', sheetSize=0.1)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=3)
    s.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0851061, 
        farPlane=0.103456, width=0.064241, height=0.0256866, cameraPosition=(
        0.0028233, 0.00286734, 0.0942809), cameraTarget=(0.0028233, 0.00286734, 
        0))
    s.Line(point1=(-0.0085, 0.014), point2=(0.006, 0.005))
    s.Line(point1=(0.006, 0.005), point2=(0.0215000000158325, 0.005))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.undo()
    s.Line(point1=(0.006, 0.005), point2=(0.02, 0.005))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FilletByRadius(radius=0.003, curve1=g[3], nearPoint1=(0.0100828651338816, 
        0.00515284668654203), curve2=g[2], nearPoint2=(0.00379665335640311, 
        0.00632593594491482))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0866605, 
        farPlane=0.101901, width=0.0533576, height=0.0213349, cameraPosition=(
        0.00598346, 0.00335491, 0.0942809), cameraTarget=(0.00598346, 
        0.00335491, 0))
    s.ConstructionLine(point1=(0.0, 0.001), point2=(0.0, -0.00150000000651926))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.ConstructionLine(point1=(-0.0015, 0.0), point2=(0.000999999965541065, 0.0))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.FixedConstraint(entity=g[6])
    s.FixedConstraint(entity=g[5])
    s.DistanceDimension(entity1=g[3], entity2=g[6], textPoint=(0.0105983540415764, 
        0.00243095937184989), value=0.0025)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='w_con', path='dimensions[1]', expression=dwcon)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='r_vert', path='dimensions[0]', expression=rvert, 
        previousParameter='w_con')
    s.AngularDimension(line1=g[3], line2=g[2], textPoint=(0.00298546627163887, 
        0.00743710529059172), value=135.0)
    s=mdb.models[nam_fem].sketches['__profile__']
    s.Parameter(name='angle', path='dimensions[2]', expression='135', 
        previousParameter='r_vert')
    s.CoincidentConstraint(entity1=v[3], entity2=g[5])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0856213, 
        farPlane=0.102941, width=0.0606336, height=0.0242442, cameraPosition=(
        0.00681019, 0.00692188, 0.0942809), cameraTarget=(0.00681019, 
        0.00692188, 0))
    s.setAsConstruction(objectList=(g[2], g[3], g[4]))
    s.Line(point1=(0.02, 0.0), point2=(-0.0132478997111321, 0.0))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.ParallelConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s.CoincidentConstraint(entity1=v[8], entity2=g[6], addUndoState=False)
    s.CoincidentConstraint(entity1=v[9], entity2=g[6], addUndoState=False)
    s.ConstructionLine(point1=(-0.0130941548589165, 0.0143515141717972), point2=(
        -0.0130941548589165, 0.0109999999701977))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[0], entity2=g[8], addUndoState=False)
    s.ConstructionLine(point1=(0.02, 0.0025), point2=(0.02, -0.00200000004749745))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[9], addUndoState=False)
    s.CoincidentConstraint(entity1=v[8], entity2=g[9])
    s.CoincidentConstraint(entity1=v[9], entity2=g[8])
    p = mdb.models[nam_fem].Part(name='Part-3', dimensionality=THREE_D, 
        type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[nam_fem].parts['Part-3']
    p.AnalyticRigidSurfExtrude(sketch=s, depth=w_ex)
    s.unsetPrimaryObject()
    p = mdb.models[nam_fem].parts['Part-3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[nam_fem].sketches['__profile__']
    p1 = mdb.models[nam_fem].parts['Part-2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    mdb.models[nam_fem].parts.changeKey(fromName='Part-2', toName='wall')
    p1 = mdb.models[nam_fem].parts['Part-3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    mdb.models[nam_fem].parts.changeKey(fromName='Part-3', toName='wall2')
    a = mdb.models[nam_fem].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models[nam_fem].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[nam_fem].parts['cell']
    a.Instance(name='cell-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.103689, 
        farPlane=0.165104, width=0.0809401, height=0.0323637, 
        viewOffsetX=0.00611489, viewOffsetY=0.000368439)
    a = mdb.models[nam_fem].rootAssembly
    p = mdb.models[nam_fem].parts['wall']
    a.Instance(name='wall-1', part=p, dependent=ON)
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall-1', ), vector=(0.0, 0.0, -0.01))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.142258, 
        farPlane=0.226895, width=0.050983, height=0.0203854, 
        viewOffsetX=0.00611876, viewOffsetY=-0.000862901)
    session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.13417, 
        farPlane=0.240329, cameraPosition=(0.141688, 0.0934977, 0.0271113), 
        cameraUpVector=(-0.765566, 0.638609, -0.0780238), cameraTarget=(
        -0.0132008, -0.000232997, -0.00884131))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.135027, 
        farPlane=0.23892, cameraPosition=(0.13843, 0.102682, 0.0132802), 
        cameraUpVector=(-0.798771, 0.596755, -0.0764704), cameraTarget=(
        -0.0132473, -0.000101908, -0.00903873))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.14671, 
        farPlane=0.2238, cameraPosition=(0.0994085, 0.0735267, 0.118178), 
        cameraUpVector=(-0.354273, 0.720436, -0.596207), cameraTarget=(
        -0.0139126, -0.000598968, -0.00725035))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.108898, 
        0.0728623, 0.109997), cameraTarget=(-0.00442261, -0.00126332, 
        -0.0154317))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall-1', ), vector=(0.0, -0.0025, 0.005))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall-1', ), vector=(0.0, 0.0025, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.132254, 
        farPlane=0.236638, width=0.120616, height=0.048228, cameraPosition=(
        0.112047, 0.0796855, 0.10312), cameraTarget=(-0.00127368, 0.00555993, 
        -0.0223091))
    p1 = mdb.models[nam_fem].parts['wall2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    a = mdb.models[nam_fem].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models[nam_fem].rootAssembly
    p = mdb.models[nam_fem].parts['wall2']
    a.Instance(name='wall2-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.125662, 
        0.0798274, 0.1119), cameraTarget=(0.00515584, 0.00100181, -0.0214817))
    a = mdb.models[nam_fem].rootAssembly
    a.rotate(instanceList=('wall2-1', ), axisPoint=(0.02, 0.0, -0.0075), 
        axisDirection=(-0.033094, 0.0, 0.0), angle=90.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.154613, 
        farPlane=0.259494, cameraPosition=(0.141158, 0.137459, 0.0192856), 
        cameraUpVector=(-0.840932, 0.453197, -0.295714), cameraTarget=(
        0.00547918, 0.00220439, -0.0234143))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.141158, 
        0.137459, 0.0192856), cameraUpVector=(-0.867853, 0.45197, -0.206287), 
        cameraTarget=(0.00547918, 0.00220439, -0.0234143))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161022, 
        farPlane=0.253861, cameraPosition=(0.119379, 0.162503, -0.0272582), 
        cameraUpVector=(-0.956058, 0.278631, -0.0912035), cameraTarget=(
        0.00442764, 0.00341356, -0.0256615))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161561, 
        farPlane=0.253379, cameraPosition=(0.116428, 0.164505, -0.0313857), 
        cameraUpVector=(-0.960522, 0.259341, -0.100696), cameraTarget=(
        0.00426884, 0.00352131, -0.0258836))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.151671, 
        farPlane=0.254753, cameraPosition=(0.139499, 0.119018, 0.0606999), 
        cameraUpVector=(-0.807555, 0.534768, -0.248753), cameraTarget=(
        0.00551321, 0.00106792, -0.0209169))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.160332, 
        farPlane=0.202775, cameraPosition=(-0.0103672, 0.0377894, 0.174944), 
        cameraUpVector=(-0.175886, 0.834391, -0.522356), cameraTarget=(
        0.000400795, -0.00170305, -0.0170197))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.152931, 
        farPlane=0.205493, cameraPosition=(-0.0284136, 0.0476211, 0.170668), 
        cameraUpVector=(-0.125077, 0.802035, -0.584034), cameraTarget=(
        0.00186459, -0.00250053, -0.0166729))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.159388, 
        farPlane=0.206657, cameraPosition=(0.0143457, 0.068053, 0.165469), 
        cameraUpVector=(-0.281519, 0.728009, -0.6251), cameraTarget=(
        -0.00220776, -0.00444644, -0.0161777))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall2-1', ), vector=(-0.003453, 0.0, 0.0075))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161454, 
        farPlane=0.204593, width=0.0708864, height=0.0283438, cameraPosition=(
        0.0214148, 0.0723307, 0.163117), cameraTarget=(0.00486135, 
        -0.000168714, -0.0185293))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.150542, 
        farPlane=0.249546, cameraPosition=(0.137582, 0.0628002, 0.106902), 
        cameraUpVector=(-0.702328, 0.706756, -0.0850394), cameraTarget=(
        -0.0035527, 0.000521592, -0.0144575))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.152349, 
        farPlane=0.26563, cameraPosition=(0.176973, 0.0793498, -0.0104802), 
        cameraUpVector=(-0.678659, 0.728208, -0.0955811), cameraTarget=(
        -0.00281138, 0.000833043, -0.0166665))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.159709, 
        farPlane=0.258268, width=0.0150924, height=0.00603468, cameraPosition=(
        0.178899, 0.0745659, -0.00572279), cameraTarget=(-0.00088582, 
        -0.00395085, -0.0119091))
    a = mdb.models[nam_fem].rootAssembly
    a.translate(instanceList=('wall2-1', ), vector=(0.0, 0.0, -1*dep))
    session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
    session.viewports['Viewport: 1'].view.setValues(session.views['Bottom'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.173867, 
        farPlane=0.216845, width=0.11085, height=0.044323, cameraPosition=(
        -0.00357352, -0.187856, -0.00909632), cameraTarget=(-0.00357352, 
        0.0075, -0.00909632))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.16473, 
        farPlane=0.22668, cameraPosition=(0.0256829, -0.157344, 0.0915733), 
        cameraUpVector=(-0.443174, 0.408614, 0.797892), cameraTarget=(
        -0.00357352, 0.0075, -0.00909632))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.163425, 
        farPlane=0.21845, cameraPosition=(-0.0198143, -0.119935, 0.138112), 
        cameraUpVector=(0.095048, 0.747093, 0.657889), cameraTarget=(
        -0.00365469, 0.00756674, -0.00901329))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.168898, 
        farPlane=0.212866, cameraPosition=(-0.00539603, -0.0442994, 0.178856), 
        cameraUpVector=(-0.15345, 0.955368, 0.25244), cameraTarget=(
        -0.00398831, 0.00581661, -0.00995607))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.161644, 
        farPlane=0.227159, cameraPosition=(0.0466918, 0.0124978, 0.178223), 
        cameraUpVector=(-0.113054, 0.993527, -0.0111199), cameraTarget=(
        -0.00520907, 0.00448548, -0.00994123))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.153241, 
        farPlane=0.241949, cameraPosition=(0.0896439, 0.0548927, 0.153168), 
        cameraUpVector=(-0.259525, 0.954769, -0.145128), cameraTarget=(
        -0.00541972, 0.00427756, -0.00981835))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.151122, 
        farPlane=0.245533, cameraPosition=(0.0992758, 0.0789758, 0.137263), 
        cameraUpVector=(-0.275579, 0.922442, -0.270475), cameraTarget=(
        -0.00531052, 0.00455059, -0.00999866))

    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models[nam_fem].parts['wall2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = mdb.models[nam_fem].parts['cell']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models[nam_fem].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    elemType1 = mesh.ElemType(elemCode=C3D20R)
    elemType2 = mesh.ElemType(elemCode=C3D15)
    elemType3 = mesh.ElemType(elemCode=C3D10)
    p = mdb.models[nam_fem].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models[nam_fem].parts['cell']
    p.seedPart(size=msh_size/3, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models[nam_fem].parts['cell']
    #p.generateMesh()
    p1 = mdb.models[nam_fem].parts['wall']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p = mdb.models[nam_fem].parts['wall']
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v1[3])
    p1 = mdb.models[nam_fem].parts['wall2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models[nam_fem].parts['wall2']
    v2, e1, d2, n1 = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v2[2])
    a = mdb.models[nam_fem].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
        adaptiveMeshConstraints=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)

    mdb.models[nam_fem].ImplicitDynamicsStep(name='Step-1', previous='Initial', 
        timePeriod=time_period_FEM, maxNumInc=1000000, application=QUASI_STATIC, 
        timeIncrementationMethod=FIXED, initialInc=init_increment_FEM, nohaf=OFF, 
        amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF, noStop=OFF, 
        nlgeom=ON)
    mdb.models['fem'].steps['Step-1'].setValues(application=DEFAULT, nohaf=OFF, 
        amplitude=STEP, initialConditions=DEFAULT)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models[nam_fem].fieldOutputRequests['F-Output-1'].setValues(
        timeInterval=time_output_FEM)
    mdb.models[nam_fem].historyOutputRequests['H-Output-1'].setValues(
        timeInterval=time_output_FEM)

    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    a = mdb.models[nam_fem].rootAssembly
    f1 = a.instances['cell-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(faces=faces1, name='esf')
    a = mdb.models[nam_fem].rootAssembly
    f1 = a.instances['cell-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#4 ]', ), )
    a.Set(faces=faces1, name='sz')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.148791, 
        farPlane=0.262383, cameraPosition=(0.1449, -0.059325, 0.0989057), 
        cameraUpVector=(-0.0388684, 0.846507, 0.530957), cameraTarget=(
        -0.00462671, 0.00247773, -0.0105736))
    a = mdb.models[nam_fem].rootAssembly
    f1 = a.instances['cell-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Set(faces=faces1, name='sy')
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='esf')
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#4 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sz')
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sy')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    a = mdb.models[nam_fem].rootAssembly
    r1 = a.instances['wall-1'].referencePoints
    refPoints1=(r1[2], )
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models[nam_fem].EncastreBC(name='encas_1', createStepName='Step-1', 
        region=region, localCsys=None)
    a = mdb.models[nam_fem].rootAssembly
    r1 = a.instances['wall2-1'].referencePoints
    refPoints1=(r1[2], )
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models[nam_fem].EncastreBC(name='encas_2', createStepName='Step-1', 
        region=region, localCsys=None)
    a = mdb.models[nam_fem].rootAssembly
    region = a.sets['sz']
    mdb.models[nam_fem].ZsymmBC(name='sym_z', createStepName='Step-1', region=region, 
        localCsys=None)
    a = mdb.models[nam_fem].rootAssembly
    region = a.sets['sy']
    mdb.models[nam_fem].YsymmBC(name='sym_y', createStepName='Step-1', region=region, 
        localCsys=None)


    ###Define contact properties
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.163227, 
        farPlane=0.204869, width=0.0412933, height=0.016511, cameraPosition=(
        0.0523839, 0.103367, 0.143173), cameraTarget=(-0.00402469, -0.00169042, 
        -0.0115687))
    mdb.models[nam_fem].ContactProperty('IntProp-1')
    mdb.models[nam_fem].interactionProperties['IntProp-1'].TangentialBehavior(
        formulation=FRICTIONLESS)
    mdb.models[nam_fem].interactionProperties['IntProp-1'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['wall-1'].faces
    side2Faces1 = s1.getSequenceFromMask(mask=('[#7 ]', ), )
    region1=regionToolset.Region(side2Faces=side2Faces1)
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region2=regionToolset.Region(side1Faces=side1Faces1)
    mdb.models[nam_fem].SurfaceToSurfaceContactStd(name='Int-1', 
        createStepName='Step-1', master=region1, slave=region2, sliding=FINITE, 
        thickness=ON, interactionProperty='IntProp-1', adjustMethod=NONE, 
        initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['wall2-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region1=regionToolset.Region(side1Faces=side1Faces1)
    a = mdb.models[nam_fem].rootAssembly
    s1 = a.instances['cell-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    region2=regionToolset.Region(side1Faces=side1Faces1)
    mdb.models[nam_fem].SurfaceToSurfaceContactStd(name='Int-2', 
        createStepName='Step-1', master=region1, slave=region2, sliding=FINITE, 
        thickness=ON, interactionProperty='IntProp-1', adjustMethod=NONE, 
        initialClearance=OMIT, datumAxis=None, clearanceRegion=None)


    #Define material properties

    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models[nam_fem].Material(name='hyp_vis')
    mdb.models[nam_fem].materials['hyp_vis'].Hyperelastic(materialType=ISOTROPIC, 
        testData=OFF, type=NEO_HOOKE, volumetricResponse=VOLUMETRIC_DATA, 
        table=((C10, D1), ))
    # mdb.models[nam_fem].materials['hyp_vis'].Viscoelastic(domain=TIME, time=PRONY, 
    #     table=((g_i, k_i, tau_i), ))
    mdb.models[nam_fem].HomogeneousSolidSection(name='cell_sec', material='hyp_vis', 
        thickness=None)
    p = mdb.models[nam_fem].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = regionToolset.Region(cells=cells)
    p = mdb.models[nam_fem].parts['cell']
    p.SectionAssignment(region=region, sectionName='cell_sec', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    mdb.models[nam_fem].materials['hyp_vis'].hyperelastic.setValues(table=((C10, 
        D1), ))
    mdb.models[nam_fem].materials['hyp_vis'].Density(table=((density, ), ))
    
    


    # import section
    # import regionToolset
    # import displayGroupMdbToolset as dgm
    # import part
    # import material
    # import assembly
    # import step
    # import interaction
    # import load
    # import mesh
    # import optimization
    # import job
    # import sketch
    # import visualization
    # import xyPlot
    # import displayGroupOdbToolset as dgo
    # import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0223823, 
        farPlane=0.0381156, width=0.0144329, height=0.00809896, 
        viewOffsetX=-0.00012662, viewOffsetY=-0.000386955)
    p = mdb.models['fem'].parts['cell']
    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
    p = mdb.models['fem'].parts['cell']
    e, d = p.edges, p.datums
    p.DatumPlaneByOffset(plane=d[6], point=p.InterestingPoint(edge=e[0], 
        rule=CENTER))
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[7], cells=pickedCells)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#3 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=STRUCTURED)
    elemType1 = mesh.ElemType(elemCode=C3D8R)
    elemType2 = mesh.ElemType(elemCode=C3D6)
    elemType3 = mesh.ElemType(elemCode=C3D4)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8H, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8H, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models['fem'].parts['cell']
    #p.generateMesh()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0224199, 
        farPlane=0.0380779, width=0.0112874, height=0.0063502, 
        viewOffsetX=-0.000197249, viewOffsetY=-0.000662914)
    p = mdb.models['fem'].parts['cell']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#2 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['fem'].parts['cell']
    e = p.edges
    p = mdb.models['fem'].parts['cell']
    p.seedPart(size=msh_size_fem, deviationFactor=0.1, minSizeFactor=0.1)
    pickedEdges = e.getSequenceFromMask(mask=('[#100 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=mesh_refin_fem, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['fem'].parts['cell']
    #p.generateMesh()

    #     #Change refinement zone
    # p = mdb.models['cfd'].parts['fluid']
    # f, e = p.faces, p.edges
    # p.DatumPlaneByOffset(plane=f[7], point=p.InterestingPoint(edge=e[14], 
    #     rule=MIDDLE))
    # p = mdb.models['cfd'].parts['fluid']
    # f1, e1, d = p.faces, p.edges, p.datums
    # p.DatumPlaneByOffset(plane=d[6], point=p.InterestingPoint(edge=e1[18], 
    #     rule=MIDDLE))
    # c = p.cells
    # pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    # p.deleteMesh(regions=pickedRegions)
    # p = mdb.models['cfd'].parts['fluid']
    # c = p.cells
    # pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    # d1 = p.datums
    # p.PartitionCellByDatumPlane(datumPlane=d1[6], cells=pickedCells)
    # p = mdb.models['cfd'].parts['fluid']
    # c = p.cells
    # pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    # d = p.datums
    # p.PartitionCellByDatumPlane(datumPlane=d[7], cells=pickedCells)
    # session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    # session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    #     meshTechnique=ON)
    # session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    #     referenceRepresentation=OFF)
    # p = mdb.models['cfd'].parts['fluid']
    # p.generateMesh()
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.227667, 
    #     farPlane=0.323622, width=0.0461408, height=0.0227797, 
    #     viewOffsetX=0.00822343, viewOffsetY=-0.00126461)
    # session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.24308, 
    #     farPlane=0.261163, width=0.0450008, height=0.0222169, 
    #     viewOffsetX=0.00943546, viewOffsetY=-0.00379473)
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.219025, 
    #     farPlane=0.291828, width=0.0405475, height=0.0200183, cameraPosition=(
    #     0.0945114, 0.058801, 0.231483), cameraUpVector=(-0.0655432, 0.978925, 
    #     -0.193417), cameraTarget=(-0.0112043, 0.00764314, 0.00838589), 
    #     viewOffsetX=0.00850173, viewOffsetY=-0.0034192)
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=0.230369, 
    #     farPlane=0.322422, width=0.0300197, height=0.0139599, 
    #     viewOffsetX=0.00397664, viewOffsetY=-0.00458711)
    # p = mdb.models['cfd'].parts['fluid']
    # c = p.cells
    # pickedRegions = c.getSequenceFromMask(mask=('[#3 ]', ), )
    # p.deleteMesh(regions=pickedRegions)
    # p = mdb.models['cfd'].parts['fluid']
    # e = p.edges
    # pickedEdges = e.getSequenceFromMask(mask=('[#b031 ]', ), )
    # p.seedEdgeBySize(edges=pickedEdges, size=mesh_refin, deviationFactor=0.1, 
    #     minSizeFactor=0.1, constraint=FINER)
    # p = mdb.models['cfd'].parts['fluid']
    # p.generateMesh()
    # p = mdb.models['cfd'].parts['fluid']
    # p.generateMesh(seedConstraintOverride=ON)


def run_cfd_i(name):
    
    work_directory = os.getcwd()
    
    try:
        os.mkdir("inputs")    
    except:
        pass
    
    os.chdir(work_directory+"\\inputs")
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import time
    
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, connectors=OFF)
    mdb.Job(name=name, model="cfd", description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, scratch='', resultsFormat=ODB, numCpus=3, numDomains=3)
    mdb.jobs[name].writeInput(consistencyChecking=OFF)

    fin = open(name+".inp", "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    #data = data.replace("1e-10, 0.5,  , 0.5, 0.5","1e-10, 1.0, 1.0, 1.0")
    data = data.replace("50, 2, 1e-05", "1000, 2, 1e-05")
    data = data.replace("250, 2, 1e-05", "1000, 2, 1e-05")
    data = data.replace("50, 2, 1e-05", "1000, 2, 1e-05")
    data = data.replace('*Fluid Boundary, type=PHYSICAL, velocity inlet, surface=sym_y', '*Fluid Boundary, type=SURFACE')
    data = data.replace('*Fluid Boundary, type=PHYSICAL, velocity inlet, surface=sym_z', '*Fluid Boundary, type=SURFACE')
    data = data.replace('VELX, 22.', '**')
    data = data.replace('VELY, 22.', '**')
    data = data.replace('VELZ, 22.', '**')
    data = data.replace('VELY, 0.', 'sym_y, VELY, 0.')
    data = data.replace('VELZ, 0.', 'sym_z, VELY, 0.')
    #data = data.replace('*Output, history, frequency=0', '*SURFACE OUTPUT, surface=esf \nTRACTION, NTRACTION, STRACTION \n*Output, history, frequency=0 \n*Element Output, elset=esf \nDENSITY, PRESSURE, PRESSFORCE, FORCE, AVGPRESS \n*SURFACE OUTPUT, SURFACE=esf \nPRESSFORCE, FORCE, AVGPRESS')

    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open(name+".inp", "wt")
    #overwrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

    #time.sleep(5)
    #os.system("abaqus job=cfd_input double cpus=3")
    # session.viewports['Viewport: 1'].setValues(displayedObject=a)
    #mdb.jobs['cfd_input'].setValues(numCpus=4, numDomains=4)
    #mdb.jobs['cfd_input'].submit(consistencyChecking=OFF)
    
    # try:
    #     with open("cfd_input.sta", "r") as fp:
    #         lines = fp.readlines()
    #         first = lines[0].split(',')[0]
    #         end = lines[-1].split(',')[0]

    #     print(first, end)
        
    #     session.mdbData.summary()
    #     o1 = session.openOdb(
    #         name='cfd_input.odb')
    #     session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    #     session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    #         variableLabel='PRESSURE', outputPosition=NODAL, )
    #     session.viewports['Viewport: 1'].odbDisplay.display.setValues(
    #         plotState=CONTOURS_ON_DEF)
    #     session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    #         'Viewport: 1', ))
    #     session.animationController.play(duration=UNLIMITED)
    #     session.animationController.stop()
    #     session.animationController.showLastFrame()       
    #     #mdb.jobs['cfd_input'].submit(consistencyChecking=OFF)
        
    # except:
    #     pass
    
    
    os.chdir(work_directory)
    
    


def cfd_write():

    ##This script writes inputs
    

    press_i = 0.00152135
    #press_i = 0.0012113
    #press_on = 0.0012113
    press_on = 0.00107842
    press_lon= 0.00125559
    
    total = 30
    
    dif = (press_i-press_on)/total ##
    n_id = 1
    x = 1
    
    #dif2 = (press_lon-press_on)/total
    
    
    ##press_com = press_lon
    press_com = press_i
    
    while x == 1:
        
        press_o = press_com-dif
        #print(press_o)
        ##press_o = press_com-dif2
        
        if n_id == total+1:
            break        
        
        if press_o == press_on:
            x = 0
            break
        
        if n_id <= 31:
            name = "cfd_"+str(n_id)
            
            md_i(press_i, press_o)
            refin_cfd()
            run_cfd_i(name)
        n_id = n_id+1
        ##press_com = press_o
        press_com = press_o
        break




def fem_act():

    from os import listdir
    from os.path import isfile, join
    #This script writes cell fem inputs
    
    cwd = os.getcwd()
    
    dir_cfd = "res_cfd"
    file = "cfd_1"
    #model_input()
    
    #os.chdir(cwddir_cfd)

    md_i(0.00152135,0.00143276)
    fem_iact()
    fem_press(dir_cfd, file)
    


def fem_iact():
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    cwd = os.getcwd()
    
    try:
        # from  abaqus import session
    
        import section
        import regionToolset
        import displayGroupMdbToolset as dgm
        import part
        import material
        import assembly
        import step
        import interaction
        import load
        import mesh
        import optimization
        import job
        import sketch
        import visualization
        import xyPlot
        import displayGroupOdbToolset as dgo
        import connectorBehavior
        
        t_per=0.001
        t_out= t_per/5
        a = mdb.models['fem'].rootAssembly
        a.regenerate()
        
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
            predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
        mdb.models['fem'].steps['Step-1'].setValues(application=QUASI_STATIC,timePeriod=t_per,timeIncrementationMethod=AUTOMATIC, 
            minInc=1e-15, nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, 
            adaptiveMeshConstraints=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
            meshTechnique=ON)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=0.166554, 
            farPlane=0.200546, width=0.026096, height=0.012165, cameraPosition=(
            0.0563074, 0.103758, 0.141477), cameraTarget=(-0.000101158, 
            -0.00129941, -0.0132644))
        p = mdb.models['fem'].parts['cell']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
            engineeringFeatures=OFF)
        #elemType1 = mesh.ElemType(elemCode=C3D20RH, elemLibrary=STANDARD)
        #elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
        #elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
        elemType1 = mesh.ElemType(elemCode=C3D8RH, elemLibrary=STANDARD, 
            kinematicSplit=AVERAGE_STRAIN, hourglassControl=DEFAULT)
        elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
        elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
        p = mdb.models['fem'].parts['cell']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
        pickedRegions =(cells, )
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
            elemType3))
        
        mdb.models['fem'].fieldOutputRequests['F-Output-1'].setValues(
            timeInterval=t_out)
        mdb.models['fem'].historyOutputRequests['H-Output-1'].setValues(
            timeInterval=t_out)
    
        p = mdb.models['fem'].parts['cell']
        p.generateMesh()

        session.mdbData.summary()
        
        
    except:
        pass
    

def fem_press(file_dir,name):
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    cwd = os.getcwd()
    
    try:
        # from  abaqus import session
        session.upgradeOdb(
            cwd+"/"+file_dir+"/"+name, 
            cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb", ) #file_dir+"/"+name.split(".")[0]+"_new.odb"
    
 
        o1 = session.openOdb(
            name=cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb")
        f = mdb.models['fem'].MappedField(name='AnalyticalField-1', description='', 
            regionType=MESH, partLevelData=False, localCsys=None, 
            positiveNormalSearchTol=5.0, boundarySearchTol=1.0)
        f.OdbMeshRegionData(
            odbFileName=cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb", 
            variableLabel='PRESSURE', stepIndex=0, frameIndex=2, 
            quantityToPlot=FIELD_OUTPUT, averageElementOutput=True, 
            useRegionBoundaries=True, regionBoundaries=ODB_REGIONS, 
            includeFeatureBoundaries=True, averageOnlyDisplayed=False, 
            computeOrder=EXTRAPOLATE_COMPUTE_AVERAGE, averagingThreshold=75.0, 
            transformationType=DEFAULT, numericForm=REAL, complexAngle=0.0, 
            featureAngle=20.0, _coordSystem=LOCAL, dataType=SCALAR, 
            displayDataType=SCALAR, outputPosition=NODAL, 
            displayOutputPosition=NODAL, refinementType=NO_REFINEMENT, 
            refinementLabel='', refinementIndex=-1, sectionPoint=())
        a = mdb.models['fem'].rootAssembly
        region = a.surfaces['esf']
        mdb.models['fem'].Pressure(name='Load-1', createStepName='Step-1', 
            region=region, distributionType=FIELD, field='AnalyticalField-1', 
            magnitude=1.0, amplitude=UNSET)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
            predefinedFields=OFF, connectors=OFF)
        mdb.Job(name='fem_'+os.path.splitext(name)[0], model='fem', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
            numGPUs=0)
        os.chdir(cwd+"/inp_cell")
        mdb.jobs['fem_'+os.path.splitext(name)[0]].writeInput(consistencyChecking=OFF)
        os.chdir(cwd)
        
    except:
        pass
    


    os.chdir(cwd) #'fem_'+os.path.splitext(name)[0]
       

def fem_i(file_dir,name):
    
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    cwd = os.getcwd()
    
    try:
        # from  abaqus import session
        session.upgradeOdb(
            cwd+"/"+file_dir+"/"+name, 
            cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb", ) #file_dir+"/"+name.split(".")[0]+"_new.odb"
    
        import section
        import regionToolset
        import displayGroupMdbToolset as dgm
        import part
        import material
        import assembly
        import step
        import interaction
        import load
        import mesh
        import optimization
        import job
        import sketch
        import visualization
        import xyPlot
        import displayGroupOdbToolset as dgo
        import connectorBehavior
        a = mdb.models['fem'].rootAssembly
        a.regenerate()
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
            predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
        mdb.models['fem'].steps['Step-1'].setValues(application=QUASI_STATIC,timeIncrementationMethod=AUTOMATIC, 
            minInc=1e-15, nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, 
            adaptiveMeshConstraints=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
            meshTechnique=ON)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=0.166554, 
            farPlane=0.200546, width=0.026096, height=0.012165, cameraPosition=(
            0.0563074, 0.103758, 0.141477), cameraTarget=(-0.000101158, 
            -0.00129941, -0.0132644))
        p = mdb.models['fem'].parts['cell']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
            engineeringFeatures=OFF)
        #elemType1 = mesh.ElemType(elemCode=C3D20RH, elemLibrary=STANDARD)
        #elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
        #elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
        elemType1 = mesh.ElemType(elemCode=C3D8RH, elemLibrary=STANDARD, 
            kinematicSplit=AVERAGE_STRAIN, hourglassControl=DEFAULT)
        elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
        elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
        p = mdb.models['fem'].parts['cell']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
        pickedRegions =(cells, )
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
            elemType3))
        p = mdb.models['fem'].parts['cell']
        p.generateMesh()
        session.Viewport(name='Viewport: 2', origin=(6.63750028610229, 
            15.4518527984619), width=399.079711914063, height=203.909271240234)
        session.viewports['Viewport: 2'].makeCurrent()
        session.viewports['Viewport: 2'].maximize()
        session.viewports['Viewport: 1'].restore()
        session.viewports['Viewport: 2'].restore()
        session.viewports['Viewport: 1'].setValues(origin=(0.0, 120.85555267334), 
            width=451.626586914063, height=105.127784729004)
        session.viewports['Viewport: 2'].setValues(origin=(0.0, 15.7277755737305), 
            width=451.626586914063, height=105.127784729004)
        session.mdbData.summary()
        o1 = session.openOdb(
            name=cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb")
        session.viewports['Viewport: 2'].setValues(displayedObject=o1)
        session.viewports['Viewport: 2'].odbDisplay.setPrimaryVariable(
            variableLabel='PRESSURE', outputPosition=NODAL, )
        session.viewports['Viewport: 2'].odbDisplay.display.setValues(
            plotState=CONTOURS_ON_DEF)
        session.viewports['Viewport: 1'].makeCurrent()
        a = mdb.models['fem'].rootAssembly
        a.regenerate()
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, loads=ON, 
            bcs=ON, predefinedFields=ON, connectors=ON)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
            meshTechnique=OFF)
        f = mdb.models['fem'].MappedField(name='AnalyticalField-1', description='', 
            regionType=MESH, partLevelData=False, localCsys=None, 
            positiveNormalSearchTol=5.0, boundarySearchTol=1.0)
        f.OdbMeshRegionData(
            odbFileName=cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb", 
            variableLabel='PRESSURE', stepIndex=0, frameIndex=2, 
            quantityToPlot=FIELD_OUTPUT, averageElementOutput=True, 
            useRegionBoundaries=True, regionBoundaries=ODB_REGIONS, 
            includeFeatureBoundaries=True, averageOnlyDisplayed=False, 
            computeOrder=EXTRAPOLATE_COMPUTE_AVERAGE, averagingThreshold=75.0, 
            transformationType=DEFAULT, numericForm=REAL, complexAngle=0.0, 
            featureAngle=20.0, _coordSystem=LOCAL, dataType=SCALAR, 
            displayDataType=SCALAR, outputPosition=NODAL, 
            displayOutputPosition=NODAL, refinementType=NO_REFINEMENT, 
            refinementLabel='', refinementIndex=-1, sectionPoint=())
        a = mdb.models['fem'].rootAssembly
        region = a.surfaces['esf']
        mdb.models['fem'].Pressure(name='Load-1', createStepName='Step-1', 
            region=region, distributionType=FIELD, field='AnalyticalField-1', 
            magnitude=1.0, amplitude=UNSET)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
            predefinedFields=OFF, connectors=OFF)
        mdb.Job(name='fem_'+os.path.splitext(name)[0], model='fem', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
            numGPUs=0)
        os.chdir(cwd+"/inp_cell")
        mdb.jobs['fem_'+os.path.splitext(name)[0]].writeInput(consistencyChecking=OFF)
        os.chdir(cwd)
        
    except:
        pass
    


    os.chdir(cwd) #'fem_'+os.path.splitext(name)[0]
    
    
def cell_write():
    
    from os import listdir
    from os.path import isfile, join
    #This script writes cell fem inputs
    
    cwd = os.getcwd()
    
    dir_cfd = "res_cfd"
    model_input()
    
    #os.chdir(cwddir_cfd)
    
    onlyfiles = [f for f in listdir(dir_cfd) if isfile(join(dir_cfd, f))]
    
    for file in onlyfiles:
    
        fem_i(dir_cfd, file)
        #print(file)
        #print(os.path.splitext(file)[0])
        #break
    
    
def cell_extract():
    
    import os, sys,subprocess, time
    from os import listdir
    from os.path import join, isfile
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import numpy as np
    
    cwd = os.getcwd()
    dir_name = "res_cell"
    
    chd = os.chdir(dir_name)
    ncwd = os.getcwd()
        
    onlyfiles = [f for f in listdir(ncwd) if isfile(join(ncwd,f)) if f.endswith(".odb")]
   
    tx=0
    try:
        resfile = [f for f in listdir(ncwd) if isfile(join(ncwd,f)) if f.endswith(".txt")]
        tx = 1
    except:
        pass
    
    #print(tx)
    #print(resfile)
    last = []
    jhh=1
    
    for files in onlyfiles:
        rrr = 0
        
        if tx == 1:
            for i in range(len(resfile)):
                #print(resfile[i].split(".")[0])
                #print("timevdisp"+files)

                if resfile[i].split(".")[0]+".odb" == "timevdisp"+files:
                    rrr = 1
                    break

        if rrr ==0:
            
            name = os.path.splitext(files)[0]
            print(name)
            
            jhh = name[name.find("x")-1]
            #print(jhh)
            
            #if jhh=="0":
            #    
            #    jhh=int(str(name[name.find("x")-2])+str(name[name.find("x")-1]))

            try:
                if isinstance(int(name[name.find("x")-2]),int)==True:
                    print("hola")
                    jhh=int(str(name[name.find("x")-2])+str(name[name.find("x")-1]))
            except:
                pass

            print(jhh)

            session.mdbData.summary()

            session.openOdb(ncwd+"/"+name+".odb")
            odb = session.odbs[ncwd+"/"+name+".odb"]

            i = 0
            u1 = [] ## front cell
            u2 = [] ## final part
            u3 = [] ## diameter
            tt = []
            #jhh=1

            while True: 
                try:
                    disp = odb.steps['Step-'+str(jhh)].frames[i].fieldOutputs['U']
                    tim  = odb.steps['Step-'+str(jhh)].frames[i].frameValue
                    u = disp.values

                    for v in u:
                        if v.nodeLabel == (7):
                            x = v.data[0]
                            u1.append(x)
                            #print(u1)
                    for v in u:
                        if v.nodeLabel == (13):
                            x = v.data[0]
                            u2.append(x)
                            #print(u1)
                    tt.append(tim)
                    for v in u:
                        if v.nodeLabel == (9):
                            x = v.data[2]
                            u3.append(x)
                            #print(u1)
                    #print(tim)
                    #print(x)
                    i = i+1
                except:
                    break

            #print tt, u1
            zipped = zip(tt,u1,u2,u3)
            
            np.savetxt("timevdisp"+name+".txt", zipped)
            
            #last.append(zipped[-1])
            
            odb.close()
    
            #if jhh==1:
            
            #jhh=jhh+1
            print(jhh)

    #np.savetxt("lpvp.txt", last)
    chd = os.chdir(cwd)
    

def cfd_act():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    name_f= "fem_cfd_19x"
    cwd = os.getcwd()
    
    mdb.Model(name='cfd_act', objectToCopy=mdb.models['cfd'])
    a = mdb.models['cfd_act'].rootAssembly

    p = mdb.models['cfd_act'].parts['fluid']
    p1 = mdb.models['cfd_act'].parts['fluid']
    p = mdb.models['cfd_act'].parts['fluid']
    p.features['Cut revolve-1'].suppress()
    
    #session.upgradeOdb(cwd+'/res_cell/'+name_f+'.odb', 
    #    cwd+'/res_cell/'+name_f+'_new.odb')
    session.openOdb(cwd+'/res_cell/'+name_f+'.odb')
    odb = session.odbs[cwd+'/res_cell/'+name_f+'.odb']
    
    p = mdb.models['cfd_act'].PartFromOdb(name='CELL-1', instance='CELL-1', 
        odb=odb, shape=DEFORMED, step=-1, frame=-1)
    p = mdb.models['cfd_act'].parts['CELL-1']
    odb.close()


    session.openOdb(cwd+'/res_cell/'+name_f+'.odb')
    odb = session.odbs[cwd+'/res_cell/'+name_f+'.odb']
    p = mdb.models['Model-1'].PartFromOdb(name='CELL-1', instance='CELL-1', 
        odb=odb, shape=DEFORMED, step=-1, frame=-1)
    p = mdb.models['Model-1'].parts['CELL-1']
    odb.close()
    import sys
    sys.path.insert(46, 
        r'E:/SIMULIA/CAE/plugins/2020/Mesh2geo')
    import mesh_geo
    mesh_geo.Run(modelName='Model-1', meshPartName='CELL-1', geoPartName='cell', 
        solid=True)
    p1 = mdb.models['cfd_act'].parts['CELL-1']
    import part
    import assembly
    import material
    import section
    import interaction
    mdb.models['cfd_act'].Part('cell', mdb.models['Model-1'].parts['cell'])
    a = mdb.models['cfd_act'].rootAssembly
    a.regenerate()
    #session.viewports['Viewport: 1'].setValues(displayedObject=a)
    #session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    #session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    #    meshTechnique=OFF)
    a = mdb.models['cfd_act'].rootAssembly
    p = mdb.models['cfd_act'].parts['cell']
    a.Instance(name='cell-1', part=p, dependent=ON)

    a1 = mdb.models['cfd_act'].rootAssembly
    
    i = 2
    x = 1
    translate = 0
    translatey = 0
    
    while x==1:
        
        jj = 0
        
        try:
            a1.InstanceFromBooleanCut(name='Part-1', 
                instanceToBeCut=mdb.models['cfd_act'].rootAssembly.instances['fluid-1'], 
                cuttingInstances=(a1.instances['cell-'+str(i-1)], ), 
                originalInstances=SUPPRESS)
            #x=2
            try:
                j=1
                while j<i:
                    a1.features['cell-'+str(j)].suppress()
                    j=j+1
            except:
                pass
            
            break

        except:

            p = mdb.models['cfd_act'].parts['cell']
            a1.Instance(name='cell-'+str(i), part=p, dependent=ON)
            a1 = mdb.models['cfd_act'].rootAssembly
            name = 'cell-'+str(i)
            translate=-0.000001*(i-1)
            
            
            translatey = translate      
            a1.translate(instanceList=(name, ), vector=(translate, translatey, 0.0))
            i=i+1
                            
            try:
                a1.features['cell-'+str(i-3)].suppress()
            except:
                pass
            

    a1.translate(instanceList=('FLUID-1', ), vector=(-translate, -translatey, 0.0))

    #Mesh size 0.0002


def fem_stp():
    
    file_dir = "res_cell"
    name = "fem_cfd_1x.odb"
    nam = name.split(".")[0]
    cwd = os.getcwd()
    
    file_dir_cfd="res_cfd"
    name_cfd = "cfd_1.odb"
    
        
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    try:
        # from  abaqus import session
        session.upgradeOdb(
            cwd+"/"+file_dir+"/"+name, 
            cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb", ) #file_dir+"/"+name.split(".")[0]+"_new.odb"

        session.upgradeOdb(
            cwd+"/"+file_dir_cfd+"/"+name_cfd, 
            cwd+"/"+file_dir_cfd+"/"+name_cfd.split(".")[0]+"_new.odb", ) #file_dir+"/"+name.split(".")[0]+"_new.odb"        
    except:
        pass
    
    try:

        mdb.Model(name='fem-stp', objectToCopy=mdb.models['fem'])
        p = mdb.models['fem-stp'].parts['cell']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        session.openOdb(cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb")
        odb = session.odbs[cwd+"/"+file_dir+"/"+name.split(".")[0]+"_new.odb"]
        p = mdb.models['fem-stp'].PartFromOdb(name='CELL-1', instance='CELL-1', 
            odb=odb, shape=DEFORMED, step=-1, frame=-1)
        p = mdb.models['fem-stp'].parts['CELL-1']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        odb.close()
        a = mdb.models['fem-stp'].rootAssembly
        #session.viewports['Viewport: 1'].setValues(displayedObject=a)
        a = mdb.models['fem-stp'].rootAssembly
        a.features['cell-1'].suppress()
        #session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
        #session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        #    meshTechnique=OFF)
        a1 = mdb.models['fem-stp'].rootAssembly
        p = mdb.models['fem-stp'].parts['CELL-1']
        a1.Instance(name='CELL-1-1', part=p, dependent=ON)
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0598673, 
        #    farPlane=0.103139, cameraPosition=(-0.032228, 0.0616331, 0.0455913), 
        #    cameraUpVector=(0.267925, 0.458227, -0.847493), cameraTarget=(
        #    0.00172643, 0.0075, -0.005))
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0639727, 
        #    farPlane=0.0990337, width=0.0203328, height=0.00951918, 
        #    cameraPosition=(-0.0372243, 0.0573177, 0.0468555), cameraTarget=(
        #    -0.00326983, 0.00318462, -0.00373576))
        a = mdb.models['fem-stp'].rootAssembly
        n1 = a.instances['CELL-1-1'].nodes
        nodes1 = n1.getSequenceFromMask(mask=(
            '[#fffffff7 #ffffffff:2 #ff #ffffc000 #3fff #0:2 #ffffff00', 
            ' #ffffffff:43 #3ffff #0:136 #fffc0000 #ffffffff:69 #3ff ]', ), )
        a.Set(nodes=nodes1, name='esf_n')
        #session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0382568, 
        #    0.0554529, 0.0481579), cameraTarget=(-0.00430232, 0.00131984, 
        #    -0.00243339))
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0703906, 
        #    farPlane=0.106891, cameraPosition=(-0.0520729, -0.0202963, 0.0599644), 
        #    cameraUpVector=(0.207276, 0.976346, 0.0615204), cameraTarget=(
        #    -0.00430232, 0.00131984, -0.00243339))
        a = mdb.models['fem-stp'].rootAssembly
        n1 = a.instances['CELL-1-1'].nodes
        nodes1 = n1.getSequenceFromMask(mask=(
            '[#1e #0:3 #ffffc000 #ffffffff:4 #3fffffff #0:90 #ffffffff:32 ]', ), )
        a.Set(nodes=nodes1, name='sy_n')
        a = mdb.models['fem-stp'].rootAssembly
        n1 = a.instances['CELL-1-1'].nodes
        nodes1 = n1.getSequenceFromMask(mask=(
            '[#fffffffd #1fffffff #0 #ffffff00 #3fff #f0000000 #ffffffff:2', 
            ' #ff #c0000000 #ffffffff:2 #fff #0:55 #fffc0000 #ffffffff:31', 
            ' #0:32 #ffffffff:57 #3ffff ]', ), )
        a.Set(nodes=nodes1, name='sz_n')
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0737406, 
        #    farPlane=0.0954006, cameraPosition=(-0.008575, 0.0355024, 0.0742183), 
        #    cameraUpVector=(-0.0146551, 0.753283, -0.657533), cameraTarget=(
        #    -0.000799741, 0.00581292, -0.00128562))
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0726581, 
        #    farPlane=0.0964829, width=0.0389512, height=0.0182358, cameraPosition=(
        #    -0.00900938, 0.0367923, 0.0736664), cameraTarget=(-0.00123412, 
        #    0.00710283, -0.00183757))
        #session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0111524, 
        #    0.0334556, 0.0747577), cameraTarget=(-0.00337712, 0.0037661, 
        #    -0.000746188))
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0715514, 
        #    farPlane=0.0954631, cameraPosition=(0.00114936, 0.0391579, 0.0725786), 
        #    cameraUpVector=(-0.0757746, 0.705888, -0.704258), cameraTarget=(
        #    -0.00293093, 0.00397293, -0.000825224))
        #session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
        #    constraints=ON, connectors=ON, engineeringFeatures=ON)
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0659446, 
        #    farPlane=0.102301, cameraPosition=(-0.03383, 0.0556109, 0.0545389), 
        #    cameraUpVector=(0.49101, 0.519394, -0.699385), cameraTarget=(
        #    -0.00377041, 0.00436779, -0.00125816))
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0629421, 
        #    farPlane=0.10854, cameraPosition=(-0.0644426, 0.0473067, 0.0328572), 
        #    cameraUpVector=(0.537214, 0.595123, -0.597687), cameraTarget=(
        #    -0.00472372, 0.00410919, -0.00193336))
        a = mdb.models['fem-stp'].rootAssembly
        region2=a.sets['esf_n']
        mdb.models['fem-stp'].interactions['Int-1'].setValues(slave=region2, 
            initialClearance=OMIT, adjustMethod=NONE, sliding=FINITE, 
            enforcement=SURFACE_TO_SURFACE, thickness=ON, 
            contactTracking=TWO_CONFIG, bondingSet=None)
        a = mdb.models['fem-stp'].rootAssembly
        region2=a.sets['esf_n']
        mdb.models['fem-stp'].interactions['Int-2'].setValues(slave=region2, 
            initialClearance=OMIT, adjustMethod=NONE, sliding=FINITE, 
            enforcement=SURFACE_TO_SURFACE, thickness=ON, 
            contactTracking=TWO_CONFIG, bondingSet=None)
        #session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        #    predefinedFields=ON, interactions=OFF, constraints=OFF, 
        #    engineeringFeatures=OFF)
        a = mdb.models['fem-stp'].rootAssembly
        region = a.sets['sy_n']
        mdb.models['fem-stp'].boundaryConditions['sym_y'].setValues(region=region)
        a = mdb.models['fem-stp'].rootAssembly
        region = a.sets['sz_n']
        mdb.models['fem-stp'].boundaryConditions['sym_z'].setValues(region=region)
        
        f1 = a.instances['CELL-1-1'].elements
        face2Elements1 = f1.getSequenceFromMask(mask=(
            '[#ffffffff:7 #3f #0:27 #c0000000 #ffffffff:24 #fff #0:97', 
            ' #fffffff0 #ffffffff:9 #ffffff ]', ), )
        face3Elements1 = f1.getSequenceFromMask(mask=(
            '[#0:1172 #fc000000 #f #3ff000 #c0000000 #ff #3ff0000', 
            ' #0 #ffc #3ff00000 #0 #ffc0 #ff000000 #3', 
            ' #ffc00 #f0000000 #3f #ffc000 #0 #3ff #ffc0000', 
            ' #0 #3ff0 #ffc00000 #0 #3ff00 #fc000000 #f', 
            ' #3ff000 #c0000000 #ff #3ff0000 #0 #ffc #3ff00000', 
            ' #0 #ffc0 #ff000000 #3 #ffc00 #f0000000 #3f', 
            ' #ffc000 #0 #3ff #ffc0000 #0 #3ff0 #ffc00000', 
            ' #0 #3ff00 #fc000000 #f #3ff000 ]', ), )
        face4Elements1 = f1.getSequenceFromMask(mask=(
            '[#0:933 #10000000 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #2108421 #0:53 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #8421084 #42108421 #10842108', 
            ' #84210842 #21084210 #8421084 #42108421 #10842108 #84210842 #21084210', 
            ' #8421084 #42108421 #10842108 #84210842 #21084210 #8421084 #42108421', 
            ' #10842108 #84210842 #21084210 #8421084 #42108421 #10842108 #84210842', 
            ' #21084210 #8421084 #42108421 #10842108 #84210842 #21084210 #8421084', 
            ' #42108421 #10842108 #84210842 #21084210 #84 ]', ), )
        a.Surface(face2Elements=face2Elements1, face3Elements=face3Elements1, 
            face4Elements=face4Elements1, name='esf_n')
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0627315, 
        #    farPlane=0.108751, width=0.0440824, height=0.020638, cameraPosition=(
        #    -0.0644214, 0.0476959, 0.0324104), cameraTarget=(-0.0047025, 0.0044984, 
        #    -0.0023802))
        #session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0740579, 
        #    farPlane=0.0889485, width=0.0291531, height=0.0136486, cameraPosition=(
        #    0.000452056, 0.00640133, 0.0765032), cameraTarget=(0.000452056, 
        #    0.00640133, -0.005))
        #session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.0015381, 
        #    0.00319936, 0.0765032), cameraTarget=(-0.0015381, 0.00319936, -0.005))
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0678461, 
        #    farPlane=0.0919847, cameraPosition=(0.0117577, 0.0231981, 0.0728848), 
        #    cameraUpVector=(-0.0771954, 0.968784, -0.23558), cameraTarget=(
        #    -0.0015381, 0.00319936, -0.005))
        #session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0667875, 
        #    farPlane=0.0930433, width=0.0489969, height=0.0229389, cameraPosition=(
        #    0.0128592, 0.0235238, 0.0726131), cameraTarget=(-0.000436582, 
        #    0.00352508, -0.00527168))
        #session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
        instances=(mdb.models['fem-stp'].rootAssembly.instances['CELL-1-1'], )
        mdb.models['fem-stp'].InitialState(updateReferenceConfiguration=ON, 
            fileName='fem_cfd_1', endStep=LAST_STEP, endIncrement=STEP_END, 
            name='Predefined Field-1', createStepName='Initial', 
            instances=instances)


        o1 = session.openOdb(
            name=cwd+"/"+file_dir_cfd+"/"+name_cfd.split(".")[0]+"_new.odb")
        f = mdb.models['fem-stp'].MappedField(name='AnalyticalField-1', description='', 
            regionType=MESH, partLevelData=False, localCsys=None, 
            positiveNormalSearchTol=5.0, boundarySearchTol=1.0)
        f.OdbMeshRegionData(
            odbFileName=cwd+"/"+file_dir_cfd+"/"+name_cfd.split(".")[0]+"_new.odb", 
            variableLabel='PRESSURE', stepIndex=0, frameIndex=2, 
            quantityToPlot=FIELD_OUTPUT, averageElementOutput=True, 
            useRegionBoundaries=True, regionBoundaries=ODB_REGIONS, 
            includeFeatureBoundaries=True, averageOnlyDisplayed=False, 
            computeOrder=EXTRAPOLATE_COMPUTE_AVERAGE, averagingThreshold=75.0, 
            transformationType=DEFAULT, numericForm=REAL, complexAngle=0.0, 
            featureAngle=20.0, _coordSystem=LOCAL, dataType=SCALAR, 
            displayDataType=SCALAR, outputPosition=NODAL, 
            displayOutputPosition=NODAL, refinementType=NO_REFINEMENT, 
            refinementLabel='', refinementIndex=-1, sectionPoint=())
        a = mdb.models['fem-stp'].rootAssembly
        region = a.surfaces['esf_n']
        mdb.models['fem-stp'].Pressure(name='Load-1', createStepName='Step-1', 
            region=region, distributionType=FIELD, field='AnalyticalField-1', 
            magnitude=1.0, amplitude=UNSET)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
            predefinedFields=OFF, connectors=OFF)
        #mdb.Job(name='fem_'+os.path.splitext(name)[0], model='fem-stp', description='', type=ANALYSIS, 
        #    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        #    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        #    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        #    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        #    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        #    numGPUs=0)
        #os.chdir(cwd+"/inp_cell")
        #mdb.jobs['fem_'+os.path.splitext(name)[0]].writeInput(consistencyChecking=OFF)
        #os.chdir(cwd)
            
    except:
        pass


#move contact = 0.0001 x

def asdg():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.18076, 
        farPlane=0.244412, width=0.0474481, height=0.0222138, 
        viewOffsetX=0.00867668, viewOffsetY=-0.0036685)
    del mdb.models['cfd_act'].rootAssembly.surfaces['esf']
    a = mdb.models['cfd_act'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#ffffffff:229 #ffff ]', ), )
    a.Surface(side1Faces=side1Faces1, name='esf')
    del mdb.models['cfd_act'].rootAssembly.sets['esf']
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['cfd_act'].parts['CELL-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = mdb.models['cfd_act'].parts['fluid']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['cfd_act'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p = mdb.models['cfd_act'].parts['Part-1']
    f, e = p.faces, p.edges
    p.DatumPlaneByOffset(plane=f[7350], point=p.InterestingPoint(edge=e[11234], 
        rule=MIDDLE))
    p = mdb.models['cfd_act'].parts['Part-1']
    f1, e1, d = p.faces, p.edges, p.datums
    p.DatumPlaneByOffset(plane=d[4], point=p.InterestingPoint(edge=e1[11221], 
        rule=MIDDLE))
    p = mdb.models['cfd_act'].parts['Part-1']
    f, e, d1 = p.faces, p.edges, p.datums
    p.DatumPlaneByOffset(plane=d1[5], point=p.InterestingPoint(edge=e[11222], 
        rule=MIDDLE))
    p = mdb.models['cfd_act'].parts['Part-1']
    f1, e1, d = p.faces, p.edges, p.datums
    p.DatumPlaneByOffset(plane=d[6], point=p.InterestingPoint(edge=e1[11226], 
        rule=MIDDLE))
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[5], cells=pickedCells)
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[6], cells=pickedCells)
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[7], cells=pickedCells)
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#8 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[4], cells=pickedCells)
    p = mdb.models['cfd_act'].parts['Part-1']
    e, d1 = p.edges, p.datums
    p.DatumPlaneByOffset(plane=d1[4], point=p.InterestingPoint(edge=e[189], 
        rule=MIDDLE))
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#10 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[12], cells=pickedCells)
    p = mdb.models['cfd_act'].parts['Part-1']
    e1, d1 = p.edges, p.datums
    p.DatumPlaneByOffset(plane=d1[12], point=p.InterestingPoint(edge=e1[201], 
        rule=MIDDLE))
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#20 ]', ), )
    d = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d[14], cells=pickedCells)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = mdb.models['cfd_act'].parts['Part-1']
    p.seedPart(size=0.00012, deviationFactor=0.1, minSizeFactor=0.1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.209271, 
        farPlane=0.246637, width=0.119386, height=0.0558929, cameraPosition=(
        -0.00958857, 0.126259, 0.189619), cameraUpVector=(0.048877, 0.625872, 
        -0.778392), cameraTarget=(-0.0073195, 0.00477975, -0.00683158))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.207261, 
        farPlane=0.248926, width=0.118239, height=0.0553559, cameraPosition=(
        -0.0219407, 0.0656261, 0.215383), cameraUpVector=(0.0430259, 0.823746, 
        -0.565325), cameraTarget=(-0.00715515, 0.00558651, -0.00717439))
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#0:11 #338000 #0:340 #4c000 ]', ), 
        )
    p.seedEdgeBySize(edges=pickedEdges, size=0.0004, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#0:6 #7c000 #0:4 #40f40 #0:340 #10000 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.0002, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#540000 #0:5 #2000 #0:3 #80000000 #80006 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.00016, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#200680 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.00014, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['cfd_act'].parts['Part-1']
    p.generateMesh()
    p = mdb.models['cfd_act'].parts['Part-1']
    p.deleteMesh()
    p = mdb.models['cfd_act'].parts['Part-1']
    p.seedPart(size=0.00014, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['cfd_act'].parts['Part-1']
    p.generateMesh()
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#20 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#0:11 #338000 #0:340 #4c000 ]', ), 
        )
    p.seedEdgeBySize(edges=pickedEdges, size=0.0008, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#4 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#0:6 #7c000 #0:4 #40600 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.0004, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#2 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#540000 #0:5 #2000 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.0002, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['cfd_act'].parts['Part-1']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.deleteMesh(regions=pickedRegions)
    p = mdb.models['cfd_act'].parts['Part-1']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#200680 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.00016, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['cfd_act'].parts['Part-1']
    p.generateMesh()
    a = mdb.models['cfd_act'].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models['cfd_act'].rootAssembly
    e1 = a.instances['Part-1-1'].elements
    elements1 = e1.getSequenceFromMask(mask=(
        '[#0:65496 #10000 #0:2 #4000 #0:2 #8000080 #1000', 
        ' #0:8 #8004000 #0:3 #20000000 #0 #4 #0', 
        ' #4000 #40000000 #82000 #0:3 #2000000 #0 #8000000', 
        ' #0:8 #8 #0:4 #a0000 #0 #90000 #0:19', 
        ' #1 #0:5 #8 #0:2 #1000000 #0 #40000', 
        ' #8000000 #0:12 #2000000 #0:3 #40000:2 #0:11 #20000', 
        ' #1 #20000000 #400 #0 #100000 #0:4 #20000000', 
        ' #0:5 #1000000 #0:2 #200000 #20000 #0:6 #2', 
        ' #0 #102000 #0:2 #80010100 #0:17 #100 #0:2', 
        ' #80000000 #1 #0:11 #20000000 #0:2 #80000000 #0:8', 
        ' #20000000 #20000 #0:3 #808000 #20 #0:18 #80', 
        ' #0:3 #200 #0:3 #100 #0:9 #201000 #0', 
        ' #1000 #0:32 #8005 #0:4 #80000 #1 #0:10', 
        ' #100 #0:4 #1000000 #20 #0 #1000 #0:4', 
        ' #40000 #40000000 #0:20 #40000 #0:5 #80000 #0:4', 
        ' #80000 #8000200 #0 #4 #8000000 #0:11 #1008', 
        ' #0:4 #80000 #0:10 #80 #0:2 #20 #0:13', 
        ' #4000 #0 #12000000 #2000 #444000 #4000000 #64444004', 
        ' #1 #12000 #80200040 #c002001 #802081 #1c004100 #40020', 
        ' #1100208 #2a0002 #400000 #8000801 #41201002 #4101000 #100080', 
        ' #400020 #0:2 #2004081 #80104020 #40004001 #420 #50', 
        ' #4000400 #2060011 #4000001 #9 #8140000 #0 #c0200', 
        ' #5820000 #10000000 #10003000 #80600002 #150020 #840000 #8001000', 
        ' #0 #2848080 #84480 #0 #400 #4000000 #0:3', 
        ' #10000 #0 #4010000 #0:4 #8000000 #0:3 #400000', 
        ' #0 #20000 #0:7 #20 #40080 #8100 #4000000', 
        ' #40020 #0:3 #420000 #400040 #20400000 #0:3 #8000000', 
        ' #0:2 #2 #1000 #20000000 #0:4 #20000000 #0:11', 
        ' #2004000 #2020000 #80000 #0 #4000000 #0 #f000000', 
        ' #6400000 #20000080 #84020801 #8010c00 #c00 #1000 #8', 
        ' #0 #801010 #1000 #40000000 #298 #8200000d #20', 
        ' #0 #10 #0 #10 #0 #2 #1000', 
        ' #21001 #40000 #0:10 #50000000 #9402101 #5411002 #10124808', 
        ' #8 #0:2 #1000000 #0:2 #40000 #600000 #400000', 
        ' #80000 #0 #30 #0 #800000 #0:2 #88000', 
        ' #8 #48 #0:8 #2000000 #20080000 #36 #0', 
        ' #8000 #0 #400 #102000 #2400004 #2082000 #80c04640', 
        ' #1000400 #d8000040 #8880600 #b0800000 #80015000 #10204000 #900000', 
        ' #4500090 #c011 #100 #0 #2010 #98430000 #8009', 
        ' #0:3 #20000 #0 #48000000 #0 #100002 #0:3', 
        ' #1000 #0 #200 #0 #20 #0 #4000000', 
        ' #2000020 #0:3 #200000 #8000000 #0:7 #4008000 #20000000', 
        ' #0:3 #72 #1010 #10000010 #0:2 #4000000 #28', 
        ' #48000200 #40000000 #89000000 #10000 #1040 #60000000 #0', 
        ' #20001 #0:4 #200000 #908600e #3892028a #8b12088 #80510041', 
        ' #897c2109 #2821 #29858204 #82024460 #41125221 #41087008 #4f0808', 
        ' #4624040a #c0234108 #56508a25 #11290002 #50300300 #10c00152 #401804a8', 
        ' #20200040 #1081122 #420e0000 #c1024a08 #660c0508 #18042344 #20290440', 
        ' #c0084214 #20000214 #142a84 #48018000 #1008c10 #2018 #20282108', 
        ' #1209a680 #4600024 #23088220 #10081301 #2414082 #0 #11c20040', 
        ' #2108000 #92838084 #d9000 #2c043c #5a28a434 #209000e1 #41040078', 
        ' #20248 #2081010 #401004 #2c690a0 #29102421 #4008a862 #83a05002', 
        ' #50002222 #14001402 #2129044 #3000340 #4104c #1a40280 #40020011', 
        ' #482220a #1000802 #80c #8040a018 #428a010 #860224 #49580002', 
        ' #1022008 #204024 #1002808 #4c10 #24018005 #8200050 #68001040', 
        ' #481342 #84804248 #cc022284 #80029810 #2042264 #30000a00 #20c41148', 
        ' #20e0108 #48000019 #a0000644 #24204000 #51089 #2180274 #420228', 
        ' #600a1104 #88820800 #20035018 #28088400 #a0e98082 #80a604 #16400a9', 
        ' #21100040 #241012 #c02005a2 #108d008 #84a50204 #1022041 #18004380', 
        ' #407c0300 #25c000 #92002200 #49460820 #24808408 #20104c80 #33650401', 
        ' #80080601 #6094820 #6a008449 #8b128030 #12003068 #8110 #400b0020', 
        ' #a0000 #42810004 #44030 #215008 #1000300 #20101000 #a1044004', 
        ' #2220880 #2000a5a2 #e0044600 #514894 #1004ae8 #a040004 #6044210', 
        ' #2c180060 #14948140 #10040428 #81010 #d0170 #a2508000 #884808', 
        ' #28000 #c4006004 #200530 #0 #90104280 #90d02480 #e00a0100', 
        ' #8a0c0 #38200085 #50460021 #4010000 #a4060100 #10061001 #5085000', 
        ' #11015510 #80200014 #6c125444 #a91a0080 #4001e202 #22400022 #888801', 
        ' #20c24000 #4958b484 #860400a9 #30308c04 #40c800 #2b068409 #8a000008', 
        ' #20082006 #8c03690c #4484804 #34020224 #2040960 #10280a42 #20080000', 
        ' #11801 #18000142 #5802 #68040508 #21230201 #90001045 #41420089', 
        ' #5854041a #c3240464 #8000686 #440 #40151801 #20041104 #6600006', 
        ' #80d85040 #80000404 #1b00248 #e40000 #651c0000 #4a043446 #12080402', 
        ' #10922481 #4480013c #2104380a #49581924 #5180200 #8232c808 #8032c1b0', 
        ' #aa00328 #42024000 #50030106 #80402028 #90293062 #48458280 #a530b58', 
        ' #1528c882 #734a45 #2001 #40c0 #a000180 #1602a00 #40004004', 
        ' #9131610 #d006800 #11304b5 #74121a01 #52000101 #880c52a4 #2031202', 
        ' #a4020404 #220d00 #82101c4 #40580a83 #90509802 #11105090 #12497044', 
        ' #508251 #2c0062e8 #40020c02 #a4006040 #870040c4 #230c480 #84812120', 
        ' #80c01410 #4000a01 #104681c #382814 #90138021 #280000 #49944508', 
        ' #4c00403e #4008800 #10000080 #12040008 #8098020 #1c01000 #50504202', 
        ' #61404989 #2040464 #7050090 #80411410 #aa814000 #b0024210 #9001118', 
        ' #82011014 #40000c #838180 #8080818a #b0122001 #300450 #900aa10', 
        ' #3298010e #2008088 #80106866 #5180a204 #a0 #c0183881 #40084200', 
        ' #21620010 #1c1 #45200008 #88202 #4b200828 #42a0000 #58020334', 
        ' #740229b0 #d004a14 #8000000 #20000800 #380000 #2002020 #28008040', 
        ' #d1000020 #448a3800 #60492000 #1a850540 #2209150 #8002500 #2004e0', 
        ' #11400084 #8815300 #14480084 #20140208 #35892a #15101111 #200c434', 
        ' #98007 #8110893 #80a310 #cc14a04 #c160c005 #8400054 #20', 
        ' #c80c504 #7800c08a #11a80020 #680a1021 #ca00404 #c2c0 #2202142', 
        ' #d3800840 #2804444 #106028 #22428042 #7a289149 #120504 #0', 
        ' #800000 #200000c #400001 #0 #4020450 #c0381502 #2041238', 
        ' #14c08002 #105c14a2 #1c21150b #68208602 #25060080 #42408000 #601', 
        ' #22804044 #8060420 #40d2000 #80411008 #8460214 #2000040 #800040a5', 
        ' #10200028 #24982005 #94828012 #8100060 #64400800 #40208c81 #54000c00', 
        ' #12001804 #4200e020 #2308088 #90006c40 #101504 #20448050 #e4000801', 
        ' #88002884 #2d018408 #a0c140 #2280a800 #142884 #50563011 #a0140228', 
        ' #6a04400 #8420c03b #800308 #1c488080 #80010000 #4000a040 #1804014', 
        ' #20000900 #4420000 #8100031 #4010010 #302860 #1aa402 #400184c1', 
        ' #20212800 #81502b8 #80c1445 #29300020 #82a4081 #11a01000 #c0a000c4', 
        ' #612000 #c101411 #ad880010 #40500610 #c01401 #18890210 #40c4424', 
        ' #8006040 #8118300 #8405000 #41408881 #824a402 #c9032221 #8404510', 
        ' #c0859412 #80403606 #4002101f #80a04904 #11c7110 #18090012 #8a900020', 
        ' #40000640 #4011122 #40220241 #40404888 #40300105 #2022842b #10800d1', 
        ' #f904622 #100e180 #40a68304 #42018 #420066d9 #52000445 #80100', 
        ' #6034014 #2003422 #60400800 #10053104 #60800f00 #a010121 #1000014', 
        ' #70800001 #108000 #1000240 #880 #80440804 #10024200 #1010210', 
        ' #440 #404000 #8800000 #400000 #40000a08 #1402024 #20000020', 
        ' #3800 #10080004 #20080000 #10000002 #80040000 #4000040 #102a8000', 
        ' #2a401845 #800088 #4110c202 #c600508 #4004a #0 #10000', 
        ' #0:10 #40000 #0:8 #800004 #0:36 #80000 #0:4', 
        ' #84000000 #40040000 #0:2 #20 #400 #1000 #40000000', 
        ' #0:24 #8000000 #10 #0:8 #80000 #0:6 #80', 
        ' #0:11 #800000 #0:41 #4000 #0:55 #10000000 #0:8', 
        ' #40000 #0:3 #1000 #0:2 #80000000 #0:53 #10000', 
        ' #0:20 #80000000 #0:4 #200 #0 #40000 #0:47', 
        ' #2000000 #0:6 #1 #0:16 #80000000 #0:13 #200000', 
        ' #0:2 #400 #0:3 #40000 #0:51 #2000000 #10', 
        ' #0:8 #20040 #0:2 #200000 #20000000 #0:2 #10000000', 
        ' #0 #10 #0 #2 #0 #80000 #0:2', ' #4000000 #0:5 #10 #0:7 #2 #80 #0:15', 
        ' #1000000 #20000 #0:4 #400 #0:2 #20000 #82100080', 
        ' #1 #0:2 #4040800 #202100 #0:3 #84000020 #0', 
        ' #2000000 #10040 #209 #0:2 #1000 #1000000 #20000', 
        ' #0:4 #2000 #c000 #0:5 #10000000 #0 #40000000', 
        ' #1 #0:3 #400 #0:2 #40000000 #400 #0', 
        ' #80 #0:13 #2000 #0:9 #20000 #0:32 #10000000', 
        ' #80000000 #400 #0:6 #200000 #2000000 #2 #0', 
        ' #2000000 #0:3 #2000000 #800400 #0:2 #800 #0:4', 
        ' #200 #2000 #1080 #0:21 #800000 #10 #0:28', 
        ' #80000 #0:5 #2010000 #0:2 #40000 #0:9 #100000:2', 
        ' #4000000 #0:2 #1000 #0:35 #200 #0:66 #40', 
        ' #14000000 #10000000 #240 #10000010 #4008000 #2900 #9200800', 
        ' #10080090 #400 #31006000 #80800000 #d0000020 #200508 #4000000', 
        ' #4030100 #60000040 #81001900 #45900600 #41004000 #308002b #40006590', 
        ' #6280010 #30100180 #4800800 #c0000 #404402 #80282401 #8100021', 
        ' #2100002 #80204 #80001 #40000000 #0 #40000610 #40000080', 
        ' #10 #0 #4c040 #8005080 #200 #40400000 #24000', 
        ' #4010102 #40804 #8020280 #4000008 #2000000 #8040000 #4000000', 
        ' #4080400 #2000 #c0601404 #821300 #10701010 #88000404 #8002c014', 
        ' #424000 #4400380 #10001841 #18000000 #420012c0 #a #0:21', 
        ' #200000 #0:43 #80000 #0:23 #2000 #804 #0:9', 
        ' #4 #0 #8001 #0:10 #2000400 #0:10 #1000000', 
        ' #40800008 #a0 #0:7 #80000000 #410000 #10 #100001', 
        ' #3 #0:9 #2000150 #42000000 #0:7 #20000 #800000', 
        ' #20080 #10002000 #800e00 #0:8 #408000 #20000020 #2012', 
        ' #88202 #0:10 #2000 #4040008 #0:7 #8000000 #0', 
        ' #80000 #20440 #80000000 #110000 #0:8 #10000000 #62210008', 
        ' #8001840 #30 #10000 #0:5 #200000 #1 #8040108', 
        ' #801040 #30006 #0 #4000000 #0:7 #80820840 #0', 
        ' #8004 #0:7 #4800000 #42000040 #1100038 #8808040 #400', 
        ' #0:5 #10000000 #0 #2000000 #81000 #1008000 #4000210', 
        ' #1 #0:3 #10000 #0:3 #10080000 #80002000 #20002', 
        ' #90 #0:8 #20000000 #4000440 #400000 #8280104 #40', 
        ' #0:8 #10400 #20200 #90000 #20240 #0:8 #18000000', 
        ' #100 #1438400 #3 #0:8 #80000 #c0000000 #40040', 
        ' #20000 #0:7 #60000 #80d0 #10400809 #0:9 #2050', 
        ' #400000 #40 #4000 #0:7 #2000000 #1080080 #5400000', 
        ' #420000 #0:8 #4400000 #2804000 #a0080010 #0:9 #40000000', 
        ' #201000 #80000 #0:18 #1000000 #0:3 #8040 #0:11', 
        ' #100 #4420000 #400000 #0:9 #40000000 #300 #4', 
        ' #0:10 #20508 #10020 #0:9 #4000000 #104 #80', 
        ' #0:2 #8 #0:5 #4000000 #80000 #2000000 #0:13', 
        ' #80106000 #0:2 #20000000 #0:24 #1000000 #40800 #0:13', 
        ' #400 #0:12 #2 #0:80 #4000 #4000000 #800000', 
        ' #0:4 #10 #0:14 #80 #0:2 #80004 #0:10', 
        ' #20000 #0:5 #20 #0:127 #100 #88004000 #8098000', 
        ' #100a8c00 #74824660 #8 #d42093 #730903c0 #1200080 #90d00008', 
        ' #28400100 #20010802 #31021008 #5020402 #35f40b0a #1802742 #18001a7', 
        ' #8000 #0:10 #1000000 #1440 #3214850 #9008508 #38404040', 
        ' #500 #0:11 #8204001 #300012 #4084040 #58010000 #4020001', 
        ' #a #0:3 #40000000 #2 #0:5 #200000 #20004280', 
        ' #40000000 #8000899 #42244520 #8808c204 #481124 #0:5 #80', 
        ' #0:3 #80000000 #0:2 #14400 #6010000 #284c00 #500a304', 
        ' #8c422c0e #194 #0:11 #4 #1040420 #8101000 #84002000', 
        ' #2a807b20 #8981c044 #3 #0 #1 #0:4 #40000', 
        ' #0:3 #2100000 #3c900011 #2850099 #10000a0 #28160802 #60000008', 
        ' #59488001 #1 #0:9 #92008000 #44001400 #2afb5010 #c0c40a44', 
        ' #32018410 #8dd04301 #e180020a #3043 #0:10 #40100000 #10000', 
        ' #8430000c #4c0c0120 #61000046 #20198108 #929c160c #2 #0:9', 
        ' #9444400 #80082001 #80200 #a8a0492 #9043020 #59006 #801030db', 
        ' #3 #0:9 #82000 #8002a40 #2690 #20108 #5f870100', 
        ' #844f04a2 #88c23120 #14188 #0:9 #c000040 #1400 #11100000', 
        ' #8202800 #10060008 #8f024001 #20c2044 #11582206 #80a #0:8', 
        ' #4 #20080000 #800084 #10110800 #41 #504291 #2a200000', 
        ' #2456202 #14062800 #12a #0:7 #8000 #0:2 #88088000', 
        ' #800 #80040a04 #a00280 #2000a004 #888004 #9202442 #0:7', 
        ' #100000 #0:2 #84000 #24000 #402000a0 #200 #20202000', 
        ' #200 #440a200a #3400044 #441 #0:9 #8000 #51000000', 
        ' #1000008 #10080098 #98014000 #6a4004 #c02000 #5042040 #0:10', 
        ' #2000080 #10310 #920000 #20004 #2020a084 #2a112000 #110200', 
        ' #42801606 #1 #0:8 #10c02001 #50000004 #8000004 #200802', 
        ' #91000281 #4302000 #88000 #21020000 #1810 #0:8 #40008000', 
        ' #0 #800800 #a008000 #41000002 #81400204 #24140000 #40089040', 
        ' #4404 #a8 #0:7 #4000000 #8100000 #20140 #901200a4', 
        ' #40006 #4000110 #1000000 #c80000 #2820000 #284400 #0:9', 
        ' #2000 #10024002 #20020000 #80182104 #1000 #100008d0 #4014912', 
        ' #8d041202 #900 #0:9 #2048100 #40020004 #2428000 #40082000', 
        ' #42080868 #28300002 #21540 #20000900 #0:8 #4000000 #0', 
        ' #2000 #40000020 #2104 #20e0000 #2f3223 #132008cb #0', 
        ' #1 #0:8 #20 #800002 #2002000 #20080080 #810', 
        ' #8010502 #4984834 #10205 #9208 #0:9 #50001000 #e1200', 
        ' #81400 #2 #40820000 #c002403 #8 #a1006012 #4', 
        ' #0:7 #8000000 #400000 #a00 #1201080 #810480 #88c300', 
        ' #3c249 #8010 #4183822 #0:9 #1000000 #10100 #89', 
        ' #882001 #80801100 #1c220081 #52040e8d #196600 #208 #0:9', 
        ' #20000280 #8004000 #3000000 #20000000 #84005000 #100000 #20001011', 
        ' #381040 #0:9 #80000000 #40040000 #80400 #800000 #1000000', 
        ' #98041000 #20902 #41002000 #80080 #0:10 #1000 #44000', 
        ' #a0000010 #20000400 #20800 #10580380 #30000020 #0:10 #80000000', 
        ' #2000000 #601000 #82000 #208083 #48028240 #9044944 #80045234', 
        ' #0:11 #40040000 #4000218 #20000130 #4404210 #d400100 #80000040', 
        ' #2162a41 #0:10 #4420000 #20000000 #200010 #80801181 #41142000', 
        ' #60 #4a034400 #5 #0:10 #21008080 #20100000 #8000c200', 
        ' #a024150 #c0a9058 #44000470 #200 #0:10 #40000000 #18002', 
        ' #80100200 #18042000 #c0615222 #380300a8 #20104044 #100010 #0:10', 
        ' #1000000 #0 #8001000 #40000000 #2010000 #40021012 #40900086', 
        ' #10000054 #0:12 #800000 #800c8400 #2080004 #604800 #20000000', 
        ' #c000401 #5 #0:8 #200000 #0 #200 #210000', 
        ' #0 #30049800 #2000220 #0 #40000000 #200 #2c01080', 
        ' #0:8 #10000000 #0:5 #4000 #4000000 #24001000 #20000', 
        ' #0:10 #40000000 #0:3 #20 #0 #1000020 #80004800', 
        ' #200000 #1000 #0:9 #1000000 #0 #4 #0:5', 
        ' #c000000 #0 #80000002 #0:9 #1000 #1000000 #0:6', 
        ' #200000 #0:10 #20 #0 #800 #0 #1000', 
        ' #0:3 #200 #0 #1000000 #40 #0:9 #10000', 
        ' #0:2 #20020000 #0:2 #200000 #0:2 #800 #10', 
        ' #400 #0:12 #2000 #0:17 #4 #0:5 #4', 
        ' #0 #20000000 #0:12 #200000 #0 #200000 #0:5', 
        ' #200000 #100000 #0:7 #80 #0:5 #1000 #2000', 
        ' #0:2 #80000 #80000000 #0:8 #8000 #0:7 #8000000', 
        ' #0 #200000 #0:2 #20000000 #20000 #0:16 #10600', 
        ' #0:6 #4004 #200000 #0:5 #8 #0:2 #40', 
        ' #0 #40 #0:2 #201 #0:7 #80000000 #20000', 
        ' #80000000 #0 #8000000 #0:2 #10000 #0:4 #800400', 
        ' #0:2 #2 #0:3 #1000 #0:4 #40000 #0:3', 
        ' #4 #2000 #200000 #100000 #2 #80000 #0:16', 
        ' #22002 #0 #8000 #100 #20000 #0:11 #100000', 
        ' #0 #100000 #8000000 #0:16 #90010008 #8e490001 #10100200', 
        ' #2006c000 #a0102 #18200800 #8000002 #4000a100 #0 #226a4000', 
        ' #200040 #400400 #1d0010 #c1800884 #1500d #d010011 #44100', 
        ' #10661013 #ce02100d #12000105 #70823001 #a0134c #90191616 #20d2188', 
        ' #8200842 #1334230 #a604d800 #3a590618 #85304101 #a604003 #61808000', 
        ' #26a4d40 #84561001 #ca5621 #8081162 #10c046 #c0aa88 #21901200', 
        ' #2103092 #c40b408c #80014044 #18102020 #22405240 #84800e50 #8033', 
        ' #2e600800 #10228280 #40046600 #642034 #4004302 #2842a006 #86cd4124', 
        ' #502e0820 #20600c00 #20400000 #1822 #824019 #22008240 #206810', 
        ' #4520a10 #43700404 #8402c104 #8c000011 #602000 #1128041 #85030100', 
        ' #821800 #3098 #10000e30 #a00001 #2130d800 #600 #40000102', 
        ' #25210280 #18048080 #4000004 #9000020 #12000 #4020a #0', 
        ' #60010080 #10500140 #4400 #204239 #0 #40228100 #4000840', 
        ' #90882 #400 #0 #4800109 #c200301 #30 #44040040', 
        ' #80000120 #10452004 #0 #48000000 #10015010 #5301 #200400', 
        ' #0 #40260010 #5104 #2000 #10000 #20038800 #8080004', 
        ' #4000500 #0 #a0080 #4 #0:2 #1803804 #10000010', 
        ' #20 #2a00000 #4 #4104 #0 #20008020 #6004000', 
        ' #0:3 #1 #220 #0:2 #1 #60000000 #600001', 
        ' #202 #0 #50000208 #800004 #1800 #80000 #410060', 
        ' #2 #0 #80 #10 #0:8 #408000 #40000000', 
        ' #0 #4 #2 #0:2 #10000 #8040 #20', 
        ' #0 #1000000 #800 #0:6 #600000 #0:2 #20000000', 
        ' #10201000 #100001 #0 #80000000 #800 #0 #2000', 
        ' #0 #800000 #0:2 #106000 #200000 #400 #0', 
        ' #40000 #0 #200020 #0 #8000000 #0:3 #100020', 
        ' #40000000 #0 #88400 #0:2 #428000 #280000 #0:2', 
        ' #40000200 #0:2 #8 #10000410 #80040 #0 #8', 
        ' #400080 #0:2 #1 #0:2 #8002000 #0 #104', 
        ' #0 #210000 #211900 #800000 #200050 #200005 #0:29', 
        ' #4000 #0 #80000000 #0:5 #800000 #0 #80', 
        ' #0:13 #8000000 #0:2 #40000000 #0:4 #20000000 #0:2', 
        ' #4000000 #0:18 #800000 #0:19 #4 #40000 #0:3', 
        ' #800 #0:13 #1 #0:4 #12000000 #20000 #0:3', 
        ' #40000000 #0 #40 #0 #2000 #0:6 #200', 
        ' #0 #1000 #0:7 #20000 #22000 #0:7 #80000', 
        ' #0:6 #80000 #80 #0 #400000 #0:5 #100', 
        ' #0 #4000000 #0:11 #80000 #0:3 #4 #0:6', 
        ' #2000 #0 #20 #1000 #0:4 #1000 #0:2', 
        ' #100 #0:4 #1 #0:2 #2 #400000 #0:8', 
        ' #100000 #0:16 #800 #0:14 #4 #0 #10400', 
        ' #0:8 #1000000 #0:3 #2000000 #0:3 #800000 #0:7', 
        ' #40 #0:6 #800000 #0:20 #2 #0:17 #8', 
        ' #0:2 #800000 #0:7 #80 #0:23 #100 #0:2', 
        ' #80000 #0:5 #100 #0:17 #20000000 #0:8 #40000000', 
        ' #0 #8 #0:6 #400 #0:13 #800000 #0:5', 
        ' #40000000 #0:6 #8 #0:9 #100000 #0 #20000000', 
        ' #0:3 #100000 #0 #80000000 #2000000 #0 #8308022', 
        ' #21100 #280400 #a06201 #a082000 #800 #4282000 #50a00004', 
        ' #0 #1100400 #4080104 #4004000 #808487 #20008435 #20', 
        ' #0:26 #40000000 #8000000 #0:5 #4000 #10 #100', 
        ' #0:2 #10000 #2000 #80000 #a100101 #c0c06 #90002020', 
        ' #102a0000 #8a8041 #28038 #a0000054 #3230 #122004 #14000', 
        ' #0:12 #1000000 #0 #10000000 #0 #4000000 #8000004', 
        ' #0:8 #8000000 #1000000 #18000080 #660009 #4100c100 #120', 
        ' #18a80000 #0:3 #1 #0:14 #1000 #0 #800000', 
        ' #0 #80080 #0:4 #2000 #0 #80000000 #0:24', 
        ' #800000 #0:2 #4 #200000 #0:4 #1 #0:10', 
        ' #10000 #0:3 #82 #0:6 #800000 #0:3 #80', 
        ' #8200000 #100000 #0:2 #10000 #221043 #a000124 #100c700', 
        ' #902802 #8300 #80 #0:3 #800020 #841 #48', 
        ' #10080000 #80080004 #30 #40 #0 #80000000 #20200042', 
        ' #20c #180044 #18001200 #2 #10000100 #4408a #0:2', 
        ' #4010 #0 #24 #4000 #c41 #9000080 #0', 
        ' #10001080 #2400500 #482400 #0 #8000000 #1000800 #20080', 
        ' #4000 #c00 #2040040 #10004208 #80009102 #10000000 #0:11', 
        ' #2400000 #7008f004 #4030 #aa0000 #2000000 #0 #4000000', 
        ' #0:11 #10b00000 #400 #c000000 #40901 #61115000 #400', 
        ' #81082480 #0:6 #80000000 #100000 #8401 #3802088 #400488', 
        ' #100000 #0:5 #2141080 #12411000 #248a0 #8102040 #100', 
        ' #0:4 #80000000 #20400083 #40000030 #4012000 #40000 #0', 
        ' #8 #0:4 #181028 #89200828 #20500012 #20101000 #a0810404', 
        ' #4000 #6000160 #0:11 #22030100 #30200 #30001 #211000', 
        ' #10400000 #88118a80 #11020853 #800100 #8020040 #811 #8000000', 
        ' #4000810 #0:11 #800000 #10088000 #8000051 #0:2 #22800', 
        ' #200600 #40000800 #8 #0:12 #80000 #0:2 #10080', 
        ' #0:2 #80302000 #10 #80 #2000 #0 #1', 
        ' #0:10 #800 #0 #1c010000 #100 #0 #10000000', 
        ' #502200 #42002 #800000 #20001000 #14 #0:4 #10', 
        ' #0:7 #10000000 #400000 #0 #8008400 #20 #400000', 
        ' #4400200 #1000001c #216c0004 #21b48000 #2024e000 #400 #2080', 
        ' #80200 #0 #10 #0:5 #c00000 #24000010 #2000000', 
        ' #1000080 #c0200 #0 #2200200 #2010000 #0:2 #200100', 
        ' #0:7 #100 #1000 #80000100 #10000 #40800000 #0:3', 
        ' #80000 #0:31 #20020 #0:10 #20 #0 #80000', 
        ' #20000 #0:41 #400000 #0:15 #80000000 #0:27 #40000000', 
        ' #10000 #0:4 #80 #0:4 #8000 #0:25 #20000000', 
        ' #0:3 #200000 #20000000 #0:10 #100 #0:9 #200', 
        ' #0:5 #4 #0:47 #1 #0 #8000 #0:22', 
        ' #210010 #0:17 #800 #0 #20000 #80 #0:9', 
        ' #10000000 #46000 #0:2 #1280 #40 #0:5 #400', 
        ' #0 #4 #0:11 #20000000 #80 #0:8 #20000000', 
        ' #2400000 #4 #10000000 #20488149 #0:20 #1000000 #421000', 
        ' #0:16 #100080 #58000 #10000080 #6001004 #10000 #80000', 
        ' #0:2 #8000000 #1000 #0:9 #40 #0:14 #1', 
        ' #8400000 #0 #81c02000 #100001 #0 #1300804 #1000080', 
        ' #0 #400 #0:5 #2 #2000000 #0:5 #400000', 
        ' #0:6 #112 #0:2 #4200000 #40682000 #240 #0', 
        ' #41000 #4082c4 #0 #249400 #0:5 #400 #0:2', 
        ' #200002 #0:11 #1000000 #230 #4000001 #8000000 #2000000', 
        ' #10 #100000 #10000040 #100001 #114 #4 #4002000', 
        ' #80000000 #0:2 #4000 #0:10 #10000 #0:4 #80100000', 
        ' #50028001 #8200000 #80000100 #0:6 #c000000 #0 #a000000', 
        ' #1000008 #181800 #0:11 #80000 #0:2 #24000020 #84008', 
        ' #0:5 #108010 #110 #0 #400000 #0:7 #400000', 
        ' #0:7 #8 #40000000 #8020 #0:17 #1000000 #0:11', 
        ' #800 #0 #2 #0 #10000000 #0:7 #200', 
        ' #0:5 #40000000 #0:2 #24080 #4891 #0 #10', 
        ' #400080 #40000 #5021200 #40 #0 #80000 #20', 
        ' #1000200 #800000 #1 #800000 #0:6 #8000000 #200', 
        ' #1000000 #0 #20 #8000 #8010 #20800003 #400', 
        ' #0:2 #400000 #80020014 #18 #1000000 #0:2 #8000000', 
        ' #0:6 #92054 #200 #40000 #200000 #0 #100:2', 
        ' #0 #8 #0:2 #8000 #8a00 #40 #10', 
        ' #0:3 #8000000 #0:2 #10 #1000 #0:9 #4000000', 
        ' #0:3 #400 #0:7 #400000 #0:4 #80000 #0', 
        ' #2000 #44 #0 #2000 #0:3 #8000800 #0:2', 
        ' #4 #40000000 #1 #0 #40 #0:13 #20000000', 
        ' #400100 #10000 #100 #80000000 #2000 #800100 #1000000', 
        ' #0 #c0002000 #0 #80100 #20000840 #48440 #2000', 
        ' #400000 #40002910 #10000000 #0:2 #10004001 #20008002 #2', 
        ' #51400 #400 #840800 #8000 #4020010 #8000401 #200', 
        ' #40 #80000000 #202000 #2008 #0 #80800000 #0:5', 
        ' #40000 #800c000 #10000 #18000 #4000 #100 #d010000', 
        ' #0 #408040 #0:4 #100 #800000 #0:8 #20', 
        ' #0:3 #80000000 #0:2 #1 #8000 #40000800 #0', 
        ' #80000000 #0:2 #1 #80000000 #4 #0 #8040000', 
        ' #10 #0:4 #40000 #8000 #80000080 #8040 #1', 
        ' #4001 #2002000 #0:2 #80000000 #0:2 #5 #0', 
        ' #4000000 #0:2 #40004000 #400 #1 #0:3 #1', 
        ' #0:3 #8000000 #60 #0:4 #2000 #0:2 #24000000', 
        ' #0:2 #80000000 #0:3 #1000000 #4 #0:3 #40000', 
        ' #0 #2000 #30100000 #500000 #8001 #200080 #0', 
        ' #1000 #2e000 #4000000 #8 #0:3 #2020000 #0:3', 
        ' #80000 #0:3 #50000 #0 #80000 #0 #4100', 
        ' #4000000 #0 #8000 #0 #10000000 #0 #10000', 
        ' #0 #22 #10000040 #0:4 #400000 #208410 #0:11', 
        ' #88000 #0:2 #400 #10 #46800000 #0 #20', 
        ' #0:4 #40000040 #0 #8000000 #0 #200 #80000000', 
        ' #0 #800000 #8000000 #8800000 #40000003 #0 #40020001', 
        ' #200008 #0:3 #90000000 #0 #22000 #0:2 #100000', 
        ' #400 #0:2 #1000000 #0:3 #10000000 #0 #80010000', 
        ' #200100 #4000000 #4 #8 #0 #2000 #0', 
        ' #20000 #0 #5000000 #0:2 #100000 #0:9 #2010000', 
        ' #80000 #0 #2000000 #2000 #40000000 #0 #100', 
        ' #0:11 #100000 #0 #10200 #20 #10000004 #0:5', 
        ' #8010 #40 #0:5 #1 #0 #800 #40000', 
        ' #300000 #10001 #0:5 #80000000 #8000000 #2000000 #0:3', 
        ' #40000000 #0:3 #20000000 #800000 #0:3 #1 #0:11', 
        ' #8000 #0 #10000 #0:2 #10001400 #40000 #8010', 
        ' #2000000 #0 #20000000 #0 #400 #2002 #0:4', 
        ' #40000 #0:8 #801 #1200 #0:10 #2000000 #0', 
        ' #80 #0 #4000 #0 #400000 #80000 #60000000', 
        ' #0:2 #1000000 #0:3 #40 #0 #200 #0:2', 
        ' #1000000 #0:3 #8000000 #0 #40080000 #0:7 #10000', 
        ' #0:3 #1000000 #0 #40010000 #0:3 #40000002 #0', 
        ' #80000 #0:7 #40000 #0:6 #10 #0:5 #2000006', 
        ' #0:17 #2000 #0:7 #8008000 #0:4 #100000 #0', 
        ' #400000 #0:2 #40000000 #0:4 #400000 #1000000 #0:10', 
        ' #12000 #0:4 #1 #0:2 #2000080 #0 #200020', 
        ' #0:8 #2 #100000 #0:17 #40000000 #90040000 #80100602', 
        ' #b8004280 #94012000 #20022300 #470104c0 #20210882 #20000 #4180019', 
        ' #40c10833 #401c1a10 #10120 #2080249 #1c024020 #25031002 #1202808', 
        ' #a30b0049 #44602210 #0:7 #80000 #0:10 #20 #0:8', 
        ' #1000000 #0:3 #80000000 #4 #0:5 #8000000 #0:7', 
        ' #10000 #0:2 #80000 #20 #0:2 #8400000 #0:2', 
        ' #2020 #0 #100 #2008000 #8020002 #10804 #100000', 
        ' #2000 #80000 #3281000 #2003 #100004 #800000 #0:2', 
        ' #804000 #298 #100020 #0 #a8802002 #800 #0', 
        ' #880000 #800 #40 #0 #400 #3000 #24060', 
        ' #0:2 #40 #1000 #3000001 #1100211 #1040 #1', 
        ' #0:2 #10000000 #0 #100 #20080000 #0 #8900400', 
        ' #0:5 #80002400 #1000 #80a20 #800 #0:4 #20', 
        ' #0:2 #1420080 #80000002 #201000 #1200800 #80202b #20010', 
        ' #84000200 #1000000 #400000 #0:7 #8000000 #80000000 #80000', 
        ' #2000 #80000 #8 #a08 #1c40 #0:8 #10000010', 
        ' #280 #10000 #86000000 #401e0000 #40 #0:14 #10000400', 
        ' #121 #2002010 #80041 #0:2 #400 #0:2 #8000000', 
        ' #0 #80 #0:8 #40000000 #80000184 #4002081 #2001000', 
        ' #40001000 #0 #4000 #0 #10029000 #80 #0:9', 
        ' #10000 #0:4 #400 #0:2 #80080 #8800010 #21', 
        ' #80 #6000000 #0 #8000 #0:12 #20000000 #0:5', 
        ' #4000000 #0:2 #10 #808000 #0:11 #1 #0:5', 
        ' #100 #0:2 #10000 #40100 #100000 #0:13 #20004', 
        ' #20000 #0:2 #8000 #0:5 #20000 #8000000 #0:12', 
        ' #1100 #0 #200000 #0 #80000000 #0:2 #404000', 
        ' #0:14 #40000 #0:6 #4000 #0:9 #60000000 #8000010', 
        ' #4011 #0:2 #20002000 #80822 #4a500 #0 #8', 
        ' #c00000 #20140 #0 #200001 #48418010 #20 #1000000', 
        ' #800 #0:4 #20 #0:5 #400000 #0:3 #2000000', 
        ' #0:3 #1008081 #44150 #4640 #c002 #10430 #2084', 
        ' #4000000 #202c00 #842c0000 #26000000 #20400006 #601008 #0', 
        ' #80010000 #80000 #83100b81 #4 #0:3 #6 #0:2', 
        ' #40000 #0:7 #2000000 #0:13 #40000 #80000000 #100', 
        ' #0:4 #2 #0 #200000 #0 #100000 #0:2', 
        ' #8000 #0:5 #800 #50000000 #40000040 #0:2 #2800008', 
        ' #0 #20 #4000000 #4000 #80420 #2021 #4000000', 
        ' #4200000 #14000001 #80018000 #22088 #0:2 #800 #2000110', 
        ' #640 #20110001 #0 #8000000 #0 #80000 #20000000', 
        ' #404001 #9001 #0:10 #100000 #0:3 #8000 #0:2', 
        ' #40080000 #0 #40000 #0:7 #200 #0:5 #8000', 
        ' #0:3 #4 #0 #40004 #0 #20010 #0', 
        ' #100 #8000000 #0:4 #1000 #0 #1440020 #11000', 
        ' #0 #10002800 #10000020 #8000 #28 #20000000 #2080', 
        ' #4002000 #84000004 #10 #20800008 #104005 #10050 #0:2', 
        ' #800048 #2000000 #0 #14400020 #86 #22240000 #4000000', 
        ' #400000 #1400110 #10000000 #1 #1020000 #8080 #0:8', 
        ' #4000000 #2000000 #0:2 #2101000 #2001 #0:3 #a4000000', 
        ' #10000 #0:2 #20000000 #800 #0 #40000 #8000000', 
        ' #301000 #8000 #0 #400 #10000000 #0:6 #20100', 
        ' #0 #20000408 #0:3 #1000 #0:3 #602800 #20000000', 
        ' #0 #80000 #0:3 #100000 #0:2 #200 #0', 
        ' #1001000 #2000 #10000008 #0:2 #800 #0 #1000010', 
        ' #0:2 #800 #10000 #0 #800001 #0:6 #40', 
        ' #0:6 #88200 #4004 #2000 #10400802 #402000c4 #60000001', 
        ' #4305c090 #982221 #a90414 #24480082 #21842045 #12043421 #82080640', 
        ' #311900d0 #84000 #911041a0 #3004050 #2080001 #40000200 #2500f5', 
        ' #8180c4 #1002008 #11001012 #2840502 #880000 #91b86080 #44000015', 
        ' #11000002 #8040000 #940904 #8851c400 #82800002 #1420400 #51858043', 
        ' #1050200 #4007080c #80024001 #90000040 #c808060c #22104003 #4001007', 
        ' #82420010 #204082 #40294040 #3c01000 #1218488 #3006001 #2', 
        ' #e80800 #2100609 #4051 #30881a #38410892 #82610 #5b010080', 
        ' #c54010 #80401c00 #6010820 #c032042 #21003040 #5580000 #c882100', 
        ' #84101000 #8010155 #8420046 #500 #84489004 #70b5800e #4a13001', 
        ' #10010432 #20200112 #4a29420 #8a6240 #100405a0 #200068 #1204142', 
        ' #80028 #8081e424 #4482 #22002004 #500121 #144a0027 #68000c03', 
        ' #80000106 #1a28000a #9084000 #5830a432 #4d880891 #580b000c #8000cd1', 
        ' #c0000803 #21802000 #28025248 #2004040 #20006400 #100 #120002', 
        ' #d00c1001 #b0002e0 #3290160 #104c0820 #228c00 #42428000 #4250606', 
        ' #8001180 #22100200 #c5048506 #8204041 #c042c08 #10c480 #410000', 
        ' #4150980 #794131 #4036444b #d0041820 #84054045 #406100aa #18094404', 
        ' #26020100 #12001048 #2190510 #b240aa10 #e188008 #4421014 #801048', 
        ' #4224006c #20000 #9007091 #c0908501 #102188 #44c00 #606', 
        ' #9408268 #54008004 #c12043c0 #168080 #10240008 #8201042 #48040c08', 
        ' #343100db #ae2128 #11048180 #70a3402 #ac0044a4 #72480100 #e1802850', 
        ' #8101102c #3400025 #11148008 #1c23112 #600 #40804211 #40c5e02', 
        ' #8549c005 #8300140 #205e0641 #21001b0 #402201c0 #80506043 #40188891', 
        ' #40840002 #a0001226 #c0035258 #51a01800 #14010410 #89641c14 #46114a14', 
        ' #8400004 #5224290a #54842 #41800008 #130a1810 #8c70101 #a062', 
        ' #80804811 #2892e400 #201c4030 #4004044 #4404c485 #2c422006 #a9140090', 
        ' #a4081880 #512163f1 #1202b202 #208002 #208d00 #1c46 #e9c000c0', 
        ' #60c08501 #804810 #9205a210 #400107a4 #5004001 #b000210 #a0041102', 
        ' #86805851 #10a00aa #10740310 #407d10 #41220002 #4500481 #20020420', 
        ' #c80a #10000 #28a810 #41422e00 #4086000 #20806080 #c0092212', 
        ' #5041a0a1 #2082800 #c001821 #1a46200 #20022 #80000900 #3312900', 
        ' #20a1800 #20087058 #8004046 #34820200 #3011041 #c0005310 #c910131', 
        ' #11818000 #11080172 #64018054 #13441102 #12089042 #c220080 #42a08650', 
        ' #4448662 #85209500 #84980000 #22190a0 #41000850 #20280d20 #18141000', 
        ' #1008282 #18802146 #18880400 #4c00531 #4c1610a6 #87410020 #7d402808', 
        ' #513100c0 #6050801 #88001400 #104c804 #405106c #10c0001 #b0080120', 
        ' #40408254 #4004 #102460 #80800400 #90102020 #210 #14406004', 
        ' #200012b #c06100 #402d1089 #81210000 #9921401 #2e008082 #8050000', 
        ' #5601a2 #6200c014 #2008416 #d8680140 #31398141 #2208800 #201004', 
        ' #2489302 #b064004 #10420a00 #f0260288 #6091002a #881e040c #12089480', 
        ' #40885060 #c1030027 #30da1319 #28418010 #1900e2 #31010304 #a002a00', 
        ' #a904b0 #1014c420 #100480 #810e0002 #210a894 #40029190 #5c84014', 
        ' #40c201c1 #51a0020 #60884000 #4420b081 #a04bc #20202a00 #21860003', 
        ' #68008000 #32022230 #4181440 #8070108 #8004200 #12c0042 #40a02294', 
        ' #c00600a8 #4200000 #30008284 #16008008 #25810202 #304 #8060019', 
        ' #80120085 #45001420 #50408101 #a0002000 #80008040 #83480280 #80002238', 
        ' #181204 #c124048 #80080488 #8338094 #45d80021 #80283780 #a0068498', 
        ' #90120c #2880841a #20b4640a #240001 #e0820281 #3008208 #4028b001', 
        ' #1d30942 #14028804 #14001029 #2a1088 #22901180 #88041823 #80024a04', 
        ' #80780230 #22100040 #2000412 #10882880 #50200004 #212d084 #84041609', 
        ' #33a1010 #c0882027 #58a80104 #22000060 #85304022 #20600000 #236080', 
        ' #132524c #842c429 #80c2628a #14430092 #41823001 #1180800 #481400', 
        ' #221110c1 #803d100 #2c20381 #20002801 #8898072 #80b4840 #80000822', 
        ' #3e1c0040 #438c9602 #80814483 #40050860 #4008004 #1280528 #80000020', 
        ' #50000c0 #a200e020 #6050020 #48808480 #2022a45 #8002040c #21420209', 
        ' #c008841 #6101000 #a0c58900 #60298088 #24118140 #a81004d0 #454500', 
        ' #40202300 #80a0800 #9a01208e #404011cf #100080bc #3800488b #200b1002', 
        ' #a0240028 #4030410 #1908a017 #83128108 #39000842 #c810890 #80000148', 
        ' #8020260 #24238098 #98810410 #509c210 #a800160 #80011120 #448a1611', 
        ' #28804a #12158011 #c0000110 #92010600 #800001 #a6108408 #23011100', 
        ' #18250828 #144c551 #79265 #6610001c #8030b240 #90840600 #29200889', 
        ' #21101240 #81a00034 #11005809 #202a0420 #a0048 #10001228 #45840400', 
        ' #32610200 #14 #81304830 #889a00d #91901201 #288c0 #400010b3', 
        ' #20048008 #888a2013 #800808 #10010100 #89380812 #60b33000 #20420004', 
        ' #4f0c58 #8b840448 #38cb1402 #28105800 #80084 #b281400 #63800000', 
        ' #40a900 #164020 #30088 #91022030 #40180 #1422c204 #8138410', 
        ' #1801a909 #d0c00088 #2808810 #48048a2c #410ba042 #244028 #c01852c2', 
        ' #90000100 #14d80a0 #900150c1 #1aa0010 #910a0100 #8114a002 #199a0020', 
        ' #ac #8b006232 #4800a010 #c6007041 #40062080 #4449e400 #104a4201', 
        ' #13000c4d #81160102 #501084c0 #8022045 #c80a302 #a124c #60103204', 
        ' #2201 #82001088 #10100802 #82050432 #36215431 #20802280 #e282114', 
        ' #a2302ac2 #84008281 #a141b #24a2818 #43094028 #a0085 #11040c00', 
        ' #a0310c12 #45000808 #a0104892 #40a05000 #64480 #40888133 #44025000', 
        ' #10444003 #10ac801 #c108210d #40000082 #500c8806 #85818900 #80061102', 
        ' #2001000 #40080050 #10d12600 #c0 #40d19100 #14020c0 #30001100', 
        ' #640c644 #88501199 #2441242c #82010 #14cc22a #43d48043 #160000', 
        ' #1001000 #0:2 #100 #0:3 #100000 #0:2 #1000', 
        ' #0 #200400 #0 #20001 #0:2 #20000000 #a000', 
        ' #100 #10 #0:5 #20000000 #0:2 #4000 #0:2', 
        ' #100000 #800 #0:8 #200000 #0:3 #28000000 #0:5', 
        ' #2042410 #0:4 #1b8 #10000:2 #400000 #0:9 #400001', 
        ' #1000000 #1000 #200 #80000040 #0:2 #80 #0:2', 
        ' #8800 #0:2 #8008000 #0:4 #1000 #0 #8001', 
        ' #0:2 #4000000 #9 #0:10 #2000 #1100 #0:6', 
        ' #40020000 #0:2 #2000 #1 #0:7 #200 #0:5', 
        ' #40 #0:11 #10 #0:2 #40 #0:18 #4000000', 
        ' #0:17 #c000 #0:37 #100000 #0:18 #10 #800100', 
        ' #0:7 #9000 #0:5 #20 #2000 #0:4 #20', 
        ' #0:25 #80000 #8000200 #0:12 #400000 #0:7 #200', 
        ' #0:30 #2000000 #0:28 #200000 #0:5 #200 #0', 
        ' #100000 #0:4 #2000000 #0:4 #40 #0:11 #10000', 
        ' #20000000 #0:6 #20 #0:6 #1000 #0:7 #2', 
        ' #0:11 #20000000 #0:8 #40000000 #0:7 #10 #0:2', 
        ' #400000 #0 #1000 #0:25 #40000000 #0:18 #1000', 
        ' #0 #2 #0:9 #400040 #0:2 #c0 #0:6', 
        ' #10000000 #0:2 #80000000 #0:6 #400 #0:26 #820', 
        ' #0:18 #4100000 #0:8 #800000 #0 #800 #0:9', 
        ' #20000000 #0 #40000000 #0 #40000000 #0:2 #1000000', 
        ' #0:2 #8000 #0:5 #2000000 #0:11 #4000 #0:21', 
        ' #2000 #0:4 #800 #0:4 #2100000 #0:4 #20000000', 
        ' #0:8 #400 #0:6 #40000000 #0:26 #10000000 #0:19', 
        ' #28000000 #0:6 #20000000 #0:16 #10000000 #0:10 #10000000', 
        ' #0:14 #200000 #0:6 #40000 #0:4 #10000000 #0:3', 
        ' #200 #0:7 #10000000 #0:22 #4000 #0:15 #10000000', 
        ' #0 #1000000 #0:4 #40 #0:13 #1000 #0:10', 
        ' #1000000 #4000 #0:6 #80000 #0:10 #20 #0', 
        ' #400 #0:10 #8000 #0:27 #20 #0:55 #40000', 
        ' #0:3 #4 #0:5 #2000 #0:7 #4b4000 #0:45', 
        ' #100 #0:3 #4 #0 #200 #0:4 #10', 
        ' #0:21 #20000 #0:3 #100 #0:3 #40 #0:16', 
        ' #74 #0:29 #4000 #0:13 #400 #0 #200', 
        ' #40 #0 #10 #0:14 #8000000 #0:10 #20000', 
        ' #0:4 #8000 #0:3 #800000 #0:11 #22000 #0:9', 
        ' #20000 #0:15 #8000000 #0:17 #40000000 #0:19 #80', 
        ' #0:40 #20000 #10000 #0:8 #41000000 #20000:2 #0:40', 
        ' #8 #0:21 #4 #0:9 #400 #0:25 #4000000', 
        ' #40 #0:39 #1 #0:8 #10000 #0:18 #20000', 
        ' #0:6 #40000000 #0:11 #4 #0:3 #80 #0:9', 
        ' #10000 #0:14 #1000000 #0:25 #4000000 #0:46 #80000000', 
        ' #0:17 #10000 #0:39 #4 #0:11 #1 #0:6', 
        ' #8000 #0:22 #10000 #0:3 #8 #0:31 #200000', 
        ' #0:39 #20 #0:27 #40000000 #0:5 #10000 #0', 
        ' #2 #0:13 #200000 #0:23 #800 #400000 #0:16', 
        ' #4 #0:24 #800000 #0:12 #20 #0:14 #4000', 
        ' #0:24 #200000 #0:32 #80000000 #0:5 #2800000 #0:22', 
        ' #2000 #0:11 #18000 #0:7 #4000 #0:20 #400', 
        ' #0:34 #240 #0:25 #2000 #0:5 #2 #0:36', 
        ' #1000000 #0:40 #1000 #0:15 #10000000 #0:6 #4000000', 
        ' #0:38 #40000000 #0:10 #800 #0:17 #80000000 #0:9', 
        ' #1 #0:3 #2000000 #40000000 #400 #0:36 #400', 
        ' #0:18 #40000 #0:6 #400 #0:58 #400 #0:31', 
        ' #10000000 #0 #400000 #0:21 #10000000 #0:29 #2', 
        ' #0:18 #8 #0:28 #2000 #8000000 #0:21 #20000', 
        ' #0:29 #400 #0:28 #1000 #0:14 #4000 #0:2', 
        ' #200000 #0:8 #100 #0:5 #20 #0:30 #1000000', 
        ' #0:9 #400 #0:2 #20000 #0:50 #2000008 #0:35', 
        ' #20000000 #0:29 #800 #0:12 #40000000 #0:27 #10000', 
        ' #0:27 #400000 #0:11 #1000000 #0:15 #4000000 #0:6', 
        ' #1000 #0:63 #800000 #0 #500000 #0:12 #40000000', 
        ' #0:47 #2 #0:6 #1 #0:7 #2 #0:43', 
        ' #40000000 #0:2 #200 #0:34 #200 #0 #800000', 
        ' #0:5 #10000 #0:5 #10000 #0:39 #100 #0:9', 
        ' #2000 #2 #0:37 #800 #0:65 #40 #0:15', 
        ' #200000 #0:15 #1000000 #0:19 #20000 #0:3 #800', 
        ' #0:42 #100000 #0:16 #8000000 #0:24 #8080000 #0:9', 
        ' #2000 #0:3 #8000000 #0:10 #1 #0:19 #8000', 
        ' #0:13 #2000 #0:37 #1000000 #0:14 #80000000 #0:2', 
        ' #400 #0:36 #80 #0:26 #800 #0:10 #4000', 
        ' #0:2 #1000000 #8000000 #0:19 #4000 #0 #1000000', 
        ' #2000 #0:21 #400000 #0:6 #1020004 #0:38 #800000', 
        ' #0:13 #800000 #8 #0:2 #8000000 #0:13 #20', 
        ' #0:2 #800 #0:9 #c000 #0:30 #200000 #0:7', 
        ' #200000 #0:37 #8 #0:4 #1 #0:13 #4000', 
        ' #0:22 #400 #100 #0 #1000000 #0:20 #2000000', 
        ' #0:23 #1000 #0:13 #80000000 #0:4 #400 #0:40', 
        ' #8000 #0:14 #80 #0:41 #100 #0:7 #8000000', 
        ' #0:44 #140 #0:21 #800000 #0:3 #200000 #0:17', 
        ' #100000 #0:15 #4000000 #0:7 #10000000 #0:3 #1000000', 
        ' #0:25 #200 #0 #20 #0 #10000 #0:9', 
        ' #40 #0:20 #8000 #0:29 #2 #0:18 #200000', 
        ' #0:47 #10 #0:20 #1000000 #0:12 #2 #0:39', 
        ' #60 #0:7 #20000000 #4 #0:12 #1000000 #0:8', 
        ' #10 #0:6 #40000000 #0:10 #14 #0:15 #208', 
        ' #0:11 #800 #0:33 #100 #0:8 #40 #0:27', 
        ' #20 #0:14 #80000 #0:9 #40000000 #0:7 #200', 
        ' #0:6 #100 #0:14 #10000000 #0:14 #8200 #0:5', 
        ' #20000 #0:7 #1 #8000000 #0:64 #80000 #0:36', 
        ' #20 #0:12 #1 #0:29 #400 #0:2 #2000', 
        ' #0:6 #200000 #0:26 #2000000 #0:5 #80000000 #0:9', 
        ' #400000 #0:48 #10 #8000000 #0:5 #4000000 #0:6', 
        ' #1000 #0:29 #2000 #0:17 #8000 #200000 #0:64', 
        ' #200040 #0:22 #400000 #0:32 #40 #80000 #0:11', 
        ' #8000000 #0:10 #10000000 #0:12 #20 #10000 #0:14', 
        ' #8 #0:62 #200000 #0:17 #400 #0:11 #40', 
        ' #0:6 #1 #0:24 #1 #0:17 #40000000 #1', 
        ' #80000 #0:12 #20000 #0:25 #800 #0:17 #200000', 
        ' #0:15 #100000 #0:33 #20000000 #0:22 #20 #0:4', 
        ' #10000000 #0:23 #2000 #0 #40000000 #0:28 #400', 
        ' #0:22 #8000000 #0:26 #4000 #0:6 #20000 #0:6', 
        ' #1000000 #0:5 #4 #0:9 #c0000 #0:5 #400000', 
        ' #0:5 #10000 #0:20 #40 #0:7 #200 #0:25', 
        ' #800000 #0:34 #4000 #0:20 #20000 #0:7 #4000000', 
        ' #0:24 #40 #0:56 #8000000 #0:39 #40 #0:62', 
        ' #2000 #0:10 #40000000 #0:13 #4000000 #0:32 #40000', 
        ' #0:11 #40000 #0:3 #10000 #2 #0:13 #8000', 
        ' #0:13 #20000 #0:19 #300000 #0:3 #4000 #0:10', 
        ' #4 #0:7 #8 #0:3 #4000 #0:2 #100', 
        ' #0:34 #800000 #0:30 #400 #0:11 #2 #0:57', 
        ' #100000 #0:26 #2000 #0:25 #100000 #0:58 #800', 
        ' #0:18 #200000 #0:29 #200 #0:10 #8 #800', 
        ' #0:2 #10000 #0:4 #80000 #0:48 #1000000 #0:7', 
        ' #2000000 #0:47 #8000000 #0:12 #400000 #0:32 #8000000', 
        ' #0:22 #200000 #0:5 #8000 #0:39 #40000 #0:87', 
        ' #20000000 #0:11 #240 #0:13 #2000000 #0:42 #4', 
        ' #0:29 #20000000 #0:18 #1400 #0 #80 #0:9', 
        ' #40 #0:5 #1 #0 #20 #0:34 #80', 
        ' #0:43 #2000 #0:10 #200 #0:8 #20000 #0:27', 
        ' #4000000 #0:21 #1000000 #0:6 #440000 #0:10 #40', 
        ' #0:4 #200 #0:2 #40000 #0:3 #10 #0:19', 
        ' #80000 #0:22 #10 #0:51 #80000000 #0:13 #10000000', 
        ' #0:14 #80000 #2000 #0:9 #200 #0:6 #4000', 
        ' #0:28 #90000000 #0:17 #20000000 #0:34 #40000000 #1', 
        ' #0:13 #400000 #0:48 #4000 #0:146 #1 #0:19', 
        ' #2000 #0:19 #20 #0:11 #80 #0:8 #100', 
        ' #0:20 #20 #0:64 #10000000 #0:21 #400000 #0:26', 
        ' #1 #0:255 #100 #0:41 #40 #0:21 #80000', 
        ' #0:4 #8000 #0:22 #40000 #0:30 #80 #0:118', 
        ' #8 #0:9 #4000000 #0:61 #80000000 #0:79 #140000', 
        ' #0:44 #80 #0:20 #1000 #0:99 #4000000 #0:9', 
        ' #100000 #0:60 #8000 #0 #40000000 #0:7 #1000', 
        ' #0:159 #20000 #0:33 #40 #0:68 #21000000 #0:5', 
        ' #4000 #0:4 #400 #0:35 #60000 #2000 #0:17', 
        ' #10000 #0:24 #8000 #0:22 #800 #1 #0:78', 
        ' #800000 #0:6 #4000 #1000000 #0:33 #100000 #0:72', 
        ' #8000 #0:4 #10 #0:25 #2000 #0:19 #400000', 
        ' #0:153 #40000000 #2 #0:10 #10 #0:39 #500', 
        ' #0 #200 #0:55 #40 #0:40 #20000000 #0:2', 
        ' #100000 #0:35 #200 #0:117 #8000000 #0:169 #20000', 
        ' #0:11 #200 #0:24 #10 #0:41 #8 #0:76', 
        ' #1 #0:21 #100000 #0:94 #8000 #0:11 #80000', 
        ' #0:20 #40000 #0:12 #8000000 #0:7 #40000 #0:116', 
        ' #80000000 #0:38 #a0000 #0:31 #800 #0:259 #50', 
        ' #0:49 #20000000 #0:78 #4000 #0:46 #4000 #0:22', 
        ' #400000 #0:197 #200000 #0:34 #100000 #0:107 #1000000', 
        ' #0:17 #d0000 #0:15 #400000 #0:95 #2 #0:2', 
        ' #100 #0:14 #80 #0:107 #1000 #0:14 #88', 
        ' #0:16 #1000000 #0:20 #2000000 #0:44 #10000 #0:55', 
        ' #4000 #0:12 #100000 #0:73 #2000 #0:62 #1000000', 
        ' #0:8 #100 #0:73 #1 #0:38 #1000 #0:31', 
        ' #40000 #0:39 #80 #0:108 #200 #0:41 #4000000', 
        ' #0 #3000000 #0:69 #8 #0:9 #8 #0:8', 
        ' #2000 #0:96 #800 #0:61 #400 #0:78 #10', 
        ' #0:24 #20000000 #0:138 #8000 #0:266 #80000000 #0:1031', 
        ' #400000 #0:141 #2000000 #0:90 #1000 #0:360 #1', 
        ' #0:555 #4000 #0:7 #40000 #0:378 #800000 #0:1637', ' #220000 ]', ), )
    a.Set(elements=elements1, name='esf')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, loads=ON, 
        bcs=ON, predefinedFields=ON, connectors=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.164682, 
        farPlane=0.260486, width=0.275192, height=0.128837, 
        viewOffsetX=0.0299299, viewOffsetY=0.0131264)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.116488, 
        farPlane=0.251464, width=0.194656, height=0.0911322, cameraPosition=(
        -0.16953, 0.0576561, 0.0811339), cameraUpVector=(0.0419354, 0.931482, 
        -0.361363), cameraTarget=(-0.01068, 0.00148891, -0.0452137), 
        viewOffsetX=0.0211709, viewOffsetY=0.00928493)
    a = mdb.models['cfd_act'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#0:230 #80000 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='input')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.163067, 
        farPlane=0.242745, width=0.272492, height=0.127572, cameraPosition=(
        0.0203225, 0.183758, 0.093648), cameraUpVector=(-0.579323, 0.467057, 
        -0.668014), cameraTarget=(-0.0323393, -0.00196293, 0.0094671), 
        viewOffsetX=0.0296363, viewOffsetY=0.0129976)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.134521, 
        farPlane=0.266903, width=0.224791, height=0.10524, cameraPosition=(
        0.116977, 0.123911, 0.0988164), cameraUpVector=(-0.359106, 0.801004, 
        -0.478995), cameraTarget=(-0.0330788, 0.00454798, 0.0117088), 
        viewOffsetX=0.0244483, viewOffsetY=0.0107223)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.1285, 
        farPlane=0.271543, width=0.21473, height=0.10053, cameraPosition=(
        0.17199, 0.0377187, 0.0712888), cameraUpVector=(-0.148159, 0.982314, 
        -0.114493), cameraTarget=(-0.0272725, 0.00097263, 0.0138747), 
        viewOffsetX=0.0233541, viewOffsetY=0.0102424)
    a = mdb.models['cfd_act'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#0:230 #40000 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='output')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.136313, 
        farPlane=0.263731, width=0.118906, height=0.055668, 
        viewOffsetX=0.0158681, viewOffsetY=0.00388373)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.148286, 
        farPlane=0.25228, width=0.12935, height=0.0605577, cameraPosition=(
        0.105078, -0.124924, 0.0921179), cameraUpVector=(0.482611, 0.774659, 
        0.408645), cameraTarget=(-0.0345005, 0.00733933, 0.0062322), 
        viewOffsetX=0.0172619, viewOffsetY=0.00422486)
    a = mdb.models['cfd_act'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2420a08 #0:229 #1000 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sym_y')
    a = mdb.models['cfd_act'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1244104 #0:229 #100000 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='sym_z')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.141752, 
        farPlane=0.25801, width=0.12365, height=0.0578894, cameraPosition=(
        0.147234, 0.00589058, 0.118123), cameraUpVector=(0.080117, 0.987004, 
        -0.139299), cameraTarget=(-0.0327896, 0.00507995, 0.00883952), 
        viewOffsetX=0.0165013, viewOffsetY=0.0040387)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.142373, 
        farPlane=0.257169, width=0.124192, height=0.0581428, cameraPosition=(
        0.136593, 0.112405, 0.080943), cameraUpVector=(-0.377884, 0.824111, 
        -0.421953), cameraTarget=(-0.0289033, 0.00153015, 0.0126068), 
        viewOffsetX=0.0165735, viewOffsetY=0.00405638)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.144917, 
        farPlane=0.256514, width=0.126411, height=0.059182, cameraPosition=(
        0.154908, 0.0713497, -0.099617), cameraUpVector=(-0.438136, 0.892968, 
        -0.103172), cameraTarget=(-0.00590502, 0.00623962, 0.0197646), 
        viewOffsetX=0.0168697, viewOffsetY=0.00412887)
    a = mdb.models['cfd_act'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#c1130d2 #0:229 #23e000 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='walls')
    import os
    os.chdir(r"D:\RAMPS\actx\inputs")


