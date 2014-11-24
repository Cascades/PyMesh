#pragma once

#include <string>
#include <vector>
#include <Wires/WireNetwork/WireNetwork.h>
#include <Wires/Parameters/ParameterManager.h>
#include "WireProfile.h"

class PhantomMeshGenerator {
    public:
        PhantomMeshGenerator(
                WireNetwork::Ptr wire_network,
                ParameterManager::Ptr manager,
                WireProfile::Ptr profile) :
            m_wire_network(wire_network),
            m_parameter_manager(manager),
            m_profile(profile) {}

    public:
        void generate();

        MatrixFr get_vertices() const { return m_vertices; }
        MatrixIr get_faces() const { return m_faces; }
        VectorI get_face_sources() const { return m_face_sources; }

        std::vector<MatrixFr> get_shape_velocities() const {
            return m_shape_velocities;
        }

    private:
        void initialize_wire_network();
        void convert_parameters_to_attributes();
        void tile();
        void convert_attributes_to_parameters();
        void inflate();
        void update_face_sources(const VectorI& face_sources);
        void compute_phantom_shape_velocity();

    private:
        WireNetwork::Ptr m_wire_network;
        WireNetwork::Ptr m_phantom_wires;

        WireProfile::Ptr m_profile;

        ParameterManager::Ptr m_parameter_manager;
        ParameterManager::Ptr m_phantom_param_manager;

        MatrixFr m_vertices;
        MatrixIr m_faces;
        VectorI  m_face_sources;
        std::vector<MatrixFr> m_shape_velocities;

        std::vector<std::string> m_thickness_roi_attr_names;
        std::vector<std::string> m_offset_roi_attr_names;
        std::vector<std::string> m_offset_derivative_attr_names;
};